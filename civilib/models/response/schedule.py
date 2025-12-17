from typing import Optional

from pydantic import Field
from ulid import ULID

from civilib.models.db.customer.customer import CustomerModel
from civilib.models.db.schedule.base import ScheduleBase
from civilib.models.db.schedule.schedule import ScheduleModel
from civilib.models.response.base import BaseResponseModel
from civilib.models.response.customer import CustomerResponseModel


class ScheduleResponseModel(BaseResponseModel, ScheduleBase):
    pagadorId: ULID = Field(default_factory=ULID, exclude=True)
    pagador: Optional[CustomerResponseModel]

    @classmethod
    def from_entities(cls, schedule: ScheduleModel, customer: Optional[CustomerModel]):
        pagador = None
        if customer:
            pagador = CustomerResponseModel.from_entity(customer)

        return cls(**schedule.to_item(), pagador=pagador)
