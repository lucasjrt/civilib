from datetime import date

from boto3.dynamodb.conditions import Attr, Key

from civilib.models.db.indexes.schedule import ScheduleIndexModel
from civilib.models.db.schedule.base import ScheduleStatus
from civilib.service.storage.dynamodb import list_dynamo_items
from civilib.service.utils import format_date


def list_schedules_for_date(target_date: date):
    condition = Key("proximaExecucao").eq(format_date(target_date))
    filter = Attr("status").eq(ScheduleStatus.ativo.value)
    return list_dynamo_items(
        condition,
        ScheduleIndexModel,
        IndexName="schedule_index",
        FilterExpression=filter,
    )
