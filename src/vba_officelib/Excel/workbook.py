from typing import TypeVar
from vba_officelib.excel.worksheets import Worksheets


T= TypeVar('T', bound='Workbook')


class Workbook:
    """
    https://learn.microsoft.com/en-us/office/vba/api/excel.workbooks
    """
    def __init__(self: T) -> None:
        self._worksheets: Worksheets

    
