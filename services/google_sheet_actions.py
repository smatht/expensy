import gspread
import pandas as pd


class GoogleSheet:
    def __init__(self, file_name, document, sheet_name):
        service_account = gspread.service_account(filename=file_name)
        sheet = service_account.open(document)
        self.sheet = sheet.worksheet(sheet_name)
        self.df_all_records = None

    def read_data(self, range):  # range = "A1:E1". Data devolvera un array de la fila 1 desde la columna A hasta la E
        data = self.sheet.get(range)
        return data

    def read_data_by_uid(self, uid):
        df = self.get_all_values()
        filtered_data = df[df['uid'] == uid]
        # devuelve un data frame de una tabla, de dos filas siendo la primera las cabeceras de las columnas
        # y la segunda los valores filtrados para acceder a un valor en concreto df["nombre"].to_string()
        return filtered_data

    def write_data(self, range, values):  # range ej "A1:V1". values must be a list of list
        self.sheet.update(range, values)

    def write_data_by_uid(self, uid, values):
        # Find the row index based on the UID
        cell = self.sheet.find(uid)
        row_index = cell.row
        # Update the row with the specified values
        self.sheet.update(f"A{row_index}:E{row_index}", values)

    def get_last_row_range(self, amount_rows: int = 1):
        last_row = len(self.sheet.get_all_values())
        deta = self.sheet.get_values()
        range_start = f"A{last_row + 1}"
        range_end = f"{chr(ord('A') + len(deta[0]) - 1)}{last_row + amount_rows}"
        return f"{range_start}:{range_end}"

    def get_all_values(self):
        if not self.df_all_records:
            data = self.sheet.get_all_records()
            self.df_all_records = pd.DataFrame(data)
        # self.sheet.get_all_values () # this return a list of list, so the get all records is easier to get values filtering
        return self.df_all_records  # this return a list of dictioraies so the key is the name column and the value is the value for that particular column
