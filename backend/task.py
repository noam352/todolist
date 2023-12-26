from typing import Optional


class Task:
    def __init__(
        self,
        description: str,
        completed: bool,
        list_id: int,
        task_id: Optional[int] = None,
    ) -> None:
        self.description = description
        self.completed = completed
        self.list_id = list_id
        self.task_id = task_id
