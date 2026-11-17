from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterator, Optional, TypeVar

from vba_officelib.excel.workbook import Workbook

T = TypeVar("T", bound="Workbooks")


class Workbooks:
    """
    VBA-compatible implementation of the Excel Workbooks collection.

    Examples
    --------
    wb = application.workbooks.add()
    wb = application.workbooks.open("test.xlsx")

    count = application.workbooks.count
    wb = application.workbooks["Book1"]
    """

    def __init__(self: T) -> None:
        self._workbooks: Dict[str, Workbook] = {}

    # ------------------------------------------------------------------
    # Collection Properties
    # ------------------------------------------------------------------

    @property
    def count(self) -> int:
        """Equivalent to VBA Workbooks.Count."""
        return len(self._workbooks)

    # ------------------------------------------------------------------
    # Collection Operations
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._workbooks)

    def __iter__(self) -> Iteratorreturn iter(self._workbooks.values())

    def __getitem__(self, key: str) -> Workbook:
        """
        Supports:

            Workbooks("Book1")
        """
        return self._workbooks[key]

    # ------------------------------------------------------------------
    # VBA Methods
    # ------------------------------------------------------------------

    def add(self: T, template: Optional[int] = None) -> Workbook:
        """
        VBA:
            Workbooks.Add([Template])

        Parameters
        ----------
        template
            Currently ignored.

        Returns
        -------
        Workbook
        """

        workbook = Workbook()

        name = f"Book{self.count + 1}"

        # Ensure uniqueness
        suffix = 1
        base_name = name

        while name in self._workbooks:
            suffix += 1
            name = f"{base_name}_{suffix}"

        workbook.name = name

        self._workbooks[name] = workbook

        return workbook

    def can_check_out(self: T, file_name: str) -> bool:
        """
        VBA:
            Workbooks.CanCheckOut

        SharePoint checkout functionality is not currently supported.
        """

        return False

    def check_out(self: T, file_name: str) -> str:
        """
        VBA:
            Workbooks.CheckOut

        Raises
        ------
        NotImplementedError
        """

        raise NotImplementedError(
            "SharePoint checkout functionality is not implemented."
        )

    def close(self: T) -> None:
        """
        VBA:
            Workbooks.Close

        Closes all open workbooks.
        """

        for workbook in list(self._workbooks.values()):
            workbook.close()

        self._workbooks.clear()

    def open(
        self: T,
        file_name: str,
        update_links: Optional[int] = None,
        read_only: bool = False,
        format: Optional[int] = None,
        password: Optional[str] = None,
        write_res_password: Optional[str] = None,
        ignore_read_only_recommended: bool = False,
        origin: Optional[int] = None,
        delimiter: Optional[str] = None,
        editable: bool = False,
        notify: bool = False,
        converter: Optional[int] = None,
        add_to_mru: bool = False,
        local: bool = False,
        corrupt_load: Optional[int] = None,
    ) -> Workbook:
        """
        VBA:
            Workbooks.Open(...)

        For now most VBA-specific options are accepted but ignored.
        """

        path = Path(file_name)

        if not path.exists():
            raise FileNotFoundError(file_name)

        workbook = Workbook.load(path)

        self._workbooks[workbook.name] = workbook

        return workbook

    def open_database(
        self: T,
        file_name: str,
        command_text: str = "",
        command_type: str = "",
        background_query: bool = False,
        import_data_as: str = "",
    ) -> Workbook:
        """
        VBA:
            Workbooks.OpenDatabase

        Intended for opening and importing database data into
        a workbook.
        """

        workbook = self.add()

        workbook.import_database(
            file_name=file_name,
            command_text=command_text,
            command_type=command_type,
            background_query=background_query,
            import_data_as=import_data_as,
        )

        return workbook

    def open_text(
        self: T,
        file_name: str,
        delimiter: str = ",",
        encoding: str = "utf-8",
    ) -> Workbook:
        """
        VBA:
            Workbooks.OpenText
        """

        workbook = self.add()

        workbook.import_text(
            file_name=file_name,
            delimiter=delimiter,
            encoding=encoding,
        )

        return workbook

    def open_xml(
        self: T,
        file_name: str,
    ) -> Workbook:
        """
        VBA:
            Workbooks.OpenXML
        """

        workbook = Workbook.load_xml(file_name)

        self._workbooks[workbook.name] = workbook

        return workbook
