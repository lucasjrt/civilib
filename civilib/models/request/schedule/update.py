from datetime import date
from decimal import Decimal
from typing import Optional

from ulid import ULID

from civilib.models.base import DynamoSerializableModel
from civilib.models.db.schedule.base import ScheduleStatus


class UpdateScheduleModel(DynamoSerializableModel):
    status: Optional[ScheduleStatus] = None
    valorBase: Optional[Decimal] = None
    pagador: Optional[ULID] = None
    vencimento: Optional[date] = None
    parcelas: Optional[int] = None
    dataInicio: Optional[date] = None
    proximaExecucao: Optional[date] = None
    parcelasEmitidas: Optional[int] = None
