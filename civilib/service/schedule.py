from ulid import ULID

from civilib.auth.context import get_context_entity
from civilib.constants import EntityType
from civilib.models.db.schedule.base import ScheduleStatus
from civilib.models.db.schedule.schedule import ScheduleModel
from civilib.models.feature import Action, Resource, Scope
from civilib.models.request.schedule.create import CreateScheduleModel
from civilib.models.request.schedule.update import UpdateScheduleModel
from civilib.service.storage.dynamodb import (
    create_dynamo_item,
    delete_dynamo_item,
    get_dynamo_item,
    get_dynamo_key,
    list_dynamo_entity,
    update_dynamo_item,
)


def get_schedule(schedule_id: ULID):
    key = get_dynamo_key(EntityType.schedule, schedule_id)
    return get_dynamo_item(key, ScheduleModel)


def list_schedules():
    return list_dynamo_entity(EntityType.schedule, ScheduleModel)


def create_schedule(schedule: CreateScheduleModel):
    scheduleId = ULID()
    model = schedule.model_dump()
    item = ScheduleModel(
        id=scheduleId,
        proximaExecucao=schedule.dataInicio,
        **model,
    )

    create_dynamo_item(item.to_item())
    return scheduleId


def update_schedule(
    schedule_id: ULID, to_update: UpdateScheduleModel, remove_from_index=False
):
    key = get_dynamo_key(EntityType.schedule, schedule_id)
    remove_paths = []
    if remove_from_index:
        remove_paths.append("proximaExecucao")
    return update_dynamo_item(key, to_update.to_item(), remove_paths=remove_paths)


def delete_schedule(schedule_id: ULID, soft_delete=True):
    if soft_delete:
        return update_schedule(
            schedule_id,
            UpdateScheduleModel(status=ScheduleStatus.cancelado),
            remove_from_index=True,
        )

    user = get_context_entity()
    if not user.has_permission(Action.write, Resource.org, Scope.all):
        raise PermissionError(
            "User does not have permission to permanently delete schedule"
        )
    key = get_dynamo_key(EntityType.schedule, schedule_id)
    delete_dynamo_item(key)
