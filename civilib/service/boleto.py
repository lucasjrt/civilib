import os
from datetime import date

import boto3
import requests
from cefapi.api import Cedente, IncluiBoletoModel, TipoPessoa, WebService
from cefapi.models import Sacado
from cefapi.models import TipoJuros as CefTipoJuros
from cefapi.models import Titulo
from dateutil.relativedelta import relativedelta

from civilib.constants import EntityType
from civilib.exceptions.errors import InvalidState
from civilib.models.common import (
    TipoDocumento,
    TipoJuros,
    get_default_juros,
    get_default_multa,
)
from civilib.models.db.boleto.base import StatusBoleto
from civilib.models.db.boleto.boleto import BoletoModel
from civilib.models.db.organization.organization import OrganizationModel
from civilib.models.request.boleto.create import CreateBoletoModel
from civilib.models.request.boleto.update import UpdateBoletoModel
from civilib.service.customer import get_customer
from civilib.service.organization import get_org, update_nosso_numero
from civilib.service.storage.dynamodb import (
    create_dynamo_item,
    get_dynamo_item,
    get_dynamo_key,
    list_dynamo_entity,
    update_dynamo_item,
)

BOLETOS_BUCKET = os.environ["BOLETOS_BUCKET"]


def get_boleto(nosso_numero: int):
    key = get_dynamo_key(EntityType.boleto, str(nosso_numero))
    return get_dynamo_item(key, BoletoModel)


def create_boleto(boleto_request: CreateBoletoModel):
    org = get_org()
    if not org:
        raise InvalidState("Org does not exist")

    nosso_numero = org.nossoNumero

    if not boleto_request.juros:
        if org.defaults:
            boleto_request.juros = org.defaults.juros
        else:
            boleto_request.juros = get_default_juros()

    if not boleto_request.multa:
        if org.defaults:
            boleto_request.multa = org.defaults.multa
        else:
            boleto_request.multa = get_default_multa()

    boleto_model = BoletoModel(
        nossoNumero=nosso_numero,
        status=[StatusBoleto.emitido],
        **boleto_request.to_item(),
    )

    cedente = create_cedente_from_org(org)
    ws = WebService(cedente)

    dados_boleto = create_inclui_boleto_model(boleto_model, cedente, org)
    boleto = ws.inclui_boleto(dados_boleto)
    print(f"Boleto recebido: {boleto}")
    dados = boleto.get("DADOS", {})
    controle = dados.get("CONTROLE_NEGOCIAL")
    codigo_retorno = controle.get("COD_RETORNO")
    if codigo_retorno == "2":
        raise InvalidState("Sistema fora do ar")

    if codigo_retorno == "1":
        mensagem = controle.get("MENSAGENS", {}).get("RETORNO")
        if mensagem.startswith("(54)"):
            raise InvalidState("Informações do cedente estão incorretas")
        raise InvalidState(f"Erro ao criar boleto: {controle.get('MSG_RETORNO')}")

    if not dados:
        raise InvalidState(f"Dados não retornados")

    inclusao = dados.get("INCLUI_BOLETO")
    url = inclusao.get("URL")
    linha_digitavel = inclusao.get("LINHA_DIGITAVEL")

    boleto_model.urlBoleto = url
    boleto_model.linhaDigitavel = linha_digitavel

    save_boleto_to_s3(nosso_numero, url)
    create_dynamo_item(boleto_model.to_item())

    update_nosso_numero(org)

    return nosso_numero


def update_boleto(nosso_numero: int, boleto: UpdateBoletoModel):
    key = get_dynamo_key(EntityType.boleto, str(nosso_numero))
    update_dynamo_item(key, boleto.to_item())


def cancel_boleto(nosso_numero: int):
    # Baixa apenas, não deleta do banco
    key = get_dynamo_key(EntityType.boleto, str(nosso_numero))
    boleto = get_dynamo_item(key, BoletoModel)
    if not boleto:
        raise InvalidState("Boleto does not exist")

    if not can_cancel_boleto(boleto):
        raise InvalidState(f"Boleto cannot be canceled. Status list: {boleto.status}")

    org = get_org()
    if not org:
        raise InvalidState("Org does not exist")

    cedente = create_cedente_from_org(org)
    ws = WebService(cedente)
    ws.baixa_boleto(nosso_numero)

    update_dynamo_item(
        key,
        {"status": boleto.status + [StatusBoleto.cancelado]},
    )


def list_boletos():
    return list_dynamo_entity(EntityType.boleto, BoletoModel)


def create_cedente_from_org(org: OrganizationModel):
    beneficiario = org.beneficiario
    if not beneficiario:
        raise InvalidState("Org beneficiario is not set")
    tipo_pessoa = TipoPessoa.Juridica
    if beneficiario.tipoDocumento == TipoDocumento.CPF:
        tipo_pessoa = TipoPessoa.Fisica

    cedente = Cedente(
        agencia=beneficiario.agencia,
        agencia_dv=beneficiario.agenciaDv,
        convenio=beneficiario.convenio,
        nome=beneficiario.nome,
        inscricao_numero=beneficiario.documento,
        inscricao_tipo=tipo_pessoa,
    )

    return cedente


def create_inclui_boleto_model(
    boleto_model: BoletoModel,
    cedente: Cedente,
    org: OrganizationModel,
):
    pagador = get_customer(boleto_model.pagadorId)
    if not pagador:
        raise InvalidState("Pagador does not exist")
    tipo_sacado = TipoPessoa.Fisica
    if pagador.tipoDocumento == TipoDocumento.CNPJ:
        tipo_sacado = TipoPessoa.Juridica

    sacado = Sacado(
        inscricao_tipo=tipo_sacado,
        inscricao_numero=pagador.documento,
        nome=pagador.nome,
        bairro=pagador.endereco.bairro or "",
        cep=pagador.endereco.cep or "",
        cidade=pagador.endereco.cidade or "",
        logradouro=pagador.endereco.logradouro or "",
        uf=pagador.endereco.uf or "",
    )

    defaults = org.defaults
    if not defaults:
        raise InvalidState("Org defaults is not set")

    juros = boleto_model.juros
    if not juros:
        juros = defaults.juros

    multa = boleto_model.multa
    if not multa:
        multa = defaults.multa

    titulo = Titulo(
        nosso_numero=org.nossoNumero,
        numero_documento=str(org.nossoNumero),
        valor=boleto_model.valor,
        vencimento=boleto_model.vencimento,
        com_qrcode=defaults.comQrcode,
        juros_mora_tipo=convert_tipo_juros(juros.tipo),
        juros_mora_data=prazo_to_date(juros.prazo, boleto_model.vencimento),
        juros_mora_valor=juros.valor,
        multa_tipo=convert_tipo_juros(multa.tipo),
        multa_data=prazo_to_date(multa.prazo, boleto_model.vencimento),
        multa_valor=multa.valor,
    )

    inclui_boleto = IncluiBoletoModel(
        cedente=cedente,
        sacado=sacado,
        titulo=titulo,
    )
    return inclui_boleto


def convert_tipo_juros(tipo_juros: TipoJuros) -> CefTipoJuros:
    if tipo_juros == TipoJuros.fixa:
        return CefTipoJuros.Fixa
    elif tipo_juros == TipoJuros.taxa:
        return CefTipoJuros.Taxa
    else:
        return CefTipoJuros.Isento


def prazo_to_date(prazo: int, vencimento: date) -> date:
    if prazo <= 0:
        prazo = 1
    return vencimento + relativedelta(days=prazo)


def can_cancel_boleto(boleto: BoletoModel) -> bool:
    return boleto.status not in {
        StatusBoleto.pago,
        StatusBoleto.cancelado,
    }


def save_boleto_to_s3(
    nosso_numero: int,
    url: str,
):
    org = get_org()
    if not org:
        raise InvalidState("Org does not exist")

    tenant_id = str(org.orgId)

    s3 = boto3.client("s3")
    boleto_file = requests.get(url)
    s3.put_object(
        Bucket=BOLETOS_BUCKET,
        Key=f"{tenant_id}/boletos/{nosso_numero}.pdf",
        Body=boleto_file.content,
        ContentType="application/pdf",
    )
