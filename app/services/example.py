from repositories.db import crud
from repositories.exceptions import ObjectExistsError
from repositories.models import Task


async def create_task(task_name: str, task_description: str) -> str:
    task = Task(name=task_name, description=task_description)
    try:
        created_task: Task = await crud.create(task)
    except ObjectExistsError as exc_info:
        return f"{exc_info}\n"
    return f"{created_task.name}\n{created_task.description}\n"


async def get_all_tasks_names() -> list[str]:
    return [task.name for task in await crud.get_all(Task)]


async def get_task_description(task_name: str) -> str:
    task = await crud.get(Task, name=task_name)
    return task[0].description
