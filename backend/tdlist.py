from typing import Optional


class TDList:
    def __init__(self, list_name: str, list_id: Optional[int] = None) -> None:
        self.list_name = list_name
        self.list_id = list_id

    def set_id(self, list_id: int):
        self.list_id = list_id
