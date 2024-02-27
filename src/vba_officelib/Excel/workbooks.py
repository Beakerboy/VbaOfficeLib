from typing import Dict, TypeVar
from vba_officelib.excel.workbook import Workbook

T = TypeVar('T', bound="Workbooks")


class Workbooks:
    def __init__(slef: T) -> None:
        self._workbooks: Dict[str, Workbook] = {}

    def add(self: T, template: int=None) -> None:
        pass

    def can_check_out(self: T, file_name: str) -> bool:
        pass

    def check_out(self: T, file_name: str) -> str:
        pass

    def close(self: T) -> None:
        pass

    def open(self: T, file_name: str=, update_links: int=, read_only: bool=,
             format=, password=, write_res_password=, ignore_read_only_command=,
             origin=, delimiter=, editable=, notify=, converter=, add_to_mru=, local=, corrupt_load=) -> Workbook:
        pass

    def OpenDatabase(self: T, file_name: str, command_text: str = , command_type: str = , background_query: str = , import_data_as: str = ) -> Workbook:
        pass

    def OpenText(self: T) -> Workbook:
        pass

    def OpenXML(self: T) -> Workbook:
        pass
