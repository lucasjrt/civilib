from datetime import date
from typing import Optional

from pydantic import Field
from ulid import ULID

from incc_shared.models.db.schedule.base import ScheduleBase


class CreateScheduleModel(ScheduleBase):
    id: ULID = Field(default_factory=ULID, exclude=True)
    proximaExecucao: Optional[date] = Field(None, exclude=True)
