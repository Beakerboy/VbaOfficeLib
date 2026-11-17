from typing import Any, TypeVar
from vba_officelib.excel.worksheets import Worksheets


T= TypeVar('T', bound='Workbook')


class Range:
    """
    https://learn.microsoft.com/en-us/office/vba/api/excel.range(object)
    """
    def __init__(self: T, cell1: string) -> None:
        self.cell = cell1
        # if cell is size one, use a single value, else an array
        self.value = null

    @property
    def value(self: T) -> Any;
        return self._workbooks
    
