from typing import Dict, Typevar


T = TypeVar('T', bound='Application')


class Application:
    def __init__(self: T) -> None;
        self._workbooks: Workbooks

    @property
    def workbooks(self: T) -> Workbooks;
        return self._workbooks
