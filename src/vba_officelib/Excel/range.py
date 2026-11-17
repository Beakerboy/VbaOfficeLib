class Range:
    """
    VBA-compatible Excel Range object.

    Represents one or more cells within a worksheet.
    """

    def __init__(
        self,
        worksheet,
        row1: int,
        col1: int,
        row2: Optional[int] = None,
        col2: Optional[int] = None,
    ) -> None:
        self._worksheet = worksheet

        self._row1 = row1
        self._col1 = col1

        self._row2 = row2 or row1
        self._col2 = col2 or col1

    # ------------------------------------------------------------------
    # VBA Properties
    # ------------------------------------------------------------------

    @property
    def Row(self) -> int:
        return self._row1

    @property
    def Column(self) -> int:
        return self._col1

    @property
    def Rows(self) -> int:
        return self._row2 - self._row1 + 1

    @property
    def Columns(self) -> int:
        return self._col2 - self._col1 + 1

    @property
    def Address(self) -> str:
        start = self._cell_address(self._row1, self._col1)
        end = self._cell_address(self._row2, self._col2)

        return start if start == end else f"{start}:{end}"

    @property
    def Value(self) -> Any:
        """
        VBA Range.Value

        Single cell => scalar
        Multi-cell => 2D list
        """

        if self.Rows == 1 and self.Columns == 1:
            return self._worksheet.get_cell(
                self._row1,
                self._col1,
            )

        result = []

        for row in range(self._row1, self._row2 + 1):
            values = []

            for col in range(self._col1, self._col2 + 1):
                values.append(
                    self._worksheet.get_cell(row, col)
                )

            result.append(values)

        return result

    @Value.setter
    def Value(self, value: Any) -> None:

        if self.Rows == 1 and self.Columns == 1:
            self._worksheet.set_cell(
                self._row1,
                self._col1,
                value,
            )
            return

        if not isinstance(value, (list, tuple)):
            raise ValueError(
                "Multi-cell Range assignment requires a 2D list."
            )

        for r, row_values in enumerate(value):
            for c, cell_value in enumerate(row_values):
                self._worksheet.set_cell(
                    self._row1 + r,
                    self._col1 + c,
                    cell_value,
                )

    @property
    def Text(self) -> str:
        value = self.Value

        return "" if value is None else str(value)

    @property
    def Count(self) -> int:
        return self.Rows * self.Columns

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def Cells(self, row: int = 1, column: int = 1) -> "Range":
        """
        VBA:
            Range.Cells(2,3)
        """

        return Range(
            self._worksheet,
            self._row1 + row - 1,
            self._col1 + column - 1,
        )

    def Offset(
        self,
        row_offset: int = 0,
        column_offset: int = 0,
    ) -> "Range":
        """
        VBA:
            Range.Offset(1,0)
        """

        return Range(
            self._worksheet,
            self._row1 + row_offset,
            self._col1 + column_offset,
            self._row2 + row_offset,
            self._col2 + column_offset,
        )

    def Resize(
        self,
        row_size: Optional[int] = None,
        column_size: Optional[int] = None,
    ) -> "Range":
        """
        VBA:
            Range.Resize(5,2)
        """

        row_size = row_size or self.Rows
        column_size = column_size or self.Columns

        return Range(
            self._worksheet,
            self._row1,
            self._col1,
            self._row1 + row_size - 1,
            self._col1 + column_size - 1,
        )

    # ------------------------------------------------------------------
    # Data Operations
    # ------------------------------------------------------------------

    def Clear(self) -> None:
        for row in range(self._row1, self._row2 + 1):
            for col in range(self._col1, self._col2 + 1):
                self._worksheet.set_cell(row, col, None)

    def ClearContents(self) -> None:
        self.Clear()

    def Copy(self, destination: Optional["Range"] = None) -> None:

        if destination is None:
            self._worksheet.application.clipboard = self.Value
            return

        destination.Value = self.Value

    def Select(self) -> None:
        self._worksheet.application.active_range = self

    # ------------------------------------------------------------------
    # Iteration
    # ------------------------------------------------------------------

    def __iter__(self) -> Iterator["Range"]:
        for row in range(self._row1, self._row2 + 1):
            for col in range(self._col1, self._col2 + 1):
                yield Range(
                    self._worksheet,
                    row,
                    col,
                )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _column_letters(column: int) -> str:
        result = ""

        while column:
            column, remainder = divmod(column - 1, 26)
            result = chr(65 + remainder) + result

        return result

    @classmethod
    def _cell_address(
        cls,
        row: int,
        column: int,
    ) -> str:
        return f"{cls._column_letters(column)}{row}"

    # ------------------------------------------------------------------
    # Debugging
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"<Range {self.Address}>"
