"""Google Sheets service for reading and writing data."""

import gspread
import pandas as pd
from typing import List, Optional


class GoogleSheet:
    """
    Google Sheets service class for data operations.

    This class provides methods to read, write, and manage data in Google
    Sheets using the gspread library and pandas for data manipulation.
    """

    def __init__(self, file_name: str, document: str, sheet_name: str):
        """
        Initialize Google Sheets connection.

        Args:
            file_name: Path to the service account JSON file
            document: Google Sheets document name or ID
            sheet_name: Name of the specific worksheet to work with
        """
        service_account = gspread.service_account(filename=file_name)
        sheet = service_account.open(document)
        self.sheet = sheet.worksheet(sheet_name)
        self.df_all_records: Optional[pd.DataFrame] = None

    def read_data(self, range_str: str) -> List[List[str]]:
        """
        Read data from a specific range in the sheet.

        Args:
            range_str: Range in A1 notation (e.g., "A1:E1")

        Returns:
            List of lists containing the data from the specified range

        Examples:
            >>> sheet.read_data("A1:E1")
            [['Header1', 'Header2', 'Header3', 'Header4', 'Header5']]
        """
        data = self.sheet.get(range_str)
        return data

    def read_data_by_uid(self, uid: str) -> pd.DataFrame:
        """
        Read data filtered by a specific UID.

        Args:
            uid: Unique identifier to filter the data

        Returns:
            DataFrame containing only the rows matching the UID

        Examples:
            >>> sheet.read_data_by_uid("user123")
            DataFrame with filtered data
        """
        df = self.get_all_values()
        filtered_data = df[df['uid'] == uid]
        return filtered_data

    def write_data(self, range_str: str, values: List[List[str]]) -> None:
        """
        Write data to a specific range in the sheet.

        Args:
            range_str: Range in A1 notation (e.g., "A1:V1")
            values: List of lists containing the data to write

        Examples:
            >>> sheet.write_data("A1:V1", [["value1", "value2", "value3"]])
        """
        self.sheet.update(range_str, values)

    def write_data_by_uid(self, uid: str, values: List[str]) -> None:
        """
        Write data to a row identified by UID.

        Args:
            uid: Unique identifier to find the target row
            values: List of values to write to the row

        Examples:
            >>> sheet.write_data_by_uid("user123", ["new_value1", "new_value2"])
        """
        # Find the row index based on the UID
        cell = self.sheet.find(uid)
        row_index = cell.row
        # Update the row with the specified values
        range_str = f"A{row_index}:E{row_index}"
        self.sheet.update(range_str, [values])

    def get_last_row_range(self, amount_rows: int = 1) -> str:
        """
        Get the range for the last row(s) in the sheet.

        Args:
            amount_rows: Number of rows to include in the range (default: 1)

        Returns:
            Range string in A1 notation for the last row(s)

        Examples:
            >>> sheet.get_last_row_range(3)
            "A100:C102"
        """
        last_row = len(self.sheet.get_all_values())
        data = self.sheet.get_values()
        range_start = f"A{last_row + 1}"
        last_col = chr(ord('A') + len(data[0]) - 1)
        range_end = f"{last_col}{last_row + amount_rows}"
        return f"{range_start}:{range_end}"

    def get_all_values(self) -> pd.DataFrame:
        """
        Get all values from the sheet as a DataFrame.

        Returns:
            DataFrame containing all records from the sheet

        Examples:
            >>> df = sheet.get_all_values()
            >>> print(df.head())
        """
        if self.df_all_records is None:
            data = self.sheet.get_all_records()
            self.df_all_records = pd.DataFrame(data)
        return self.df_all_records
