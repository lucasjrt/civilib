from pydantic import BaseModel


class SyncBoletoModel(BaseModel):
    nosso_numero: int
