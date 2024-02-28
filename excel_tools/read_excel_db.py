import sqlite3
from icecream import ic
import pandas as pd

from files_features import output_message_exit


def read_xlsx_to_db(db_file_name: str, xlsx_file: str):
    connection = sqlite3.connect(db_file_name)
    sheets = pd.ExcelFile(xlsx_file).sheet_names
    n = 3
    ic(sheets[:n])              # ['Quote', 'Attributes', 'Options'] ['Resources', 'Attributes', 'Options']
    for sheet in sheets[:n]:
        df = pd.read_excel(xlsx_file, sheet_name=sheet, dtype="object")  # encoding='utf-8' header=None,
        if not df.empty:
            row_max = df.shape[0] - 1
            column_max = df.shape[1] - 1
            ic(sheet, row_max, column_max)
        else:
            output_message_exit("нет исходных данных", f"файл: {xlsx_file} страница: {sheet}")
        connection.execute(f"DROP TABLE IF EXISTS {sheet};")
        df.to_sql(sheet, connection, if_exists='replace', index=False)
        connection.commit()
    connection.close()
    ic("данные прочитаны в БД")


if __name__ == '__main__':
    import os
    db_name = r"C:\Users\kazak.ke\Documents\PythonProjects\QuotesReportCard\DB\parameters.sqlite3"
    path = r"C:\Users\kazak.ke\Documents\PythonProjects\QuotesReportCard\src"
    file_name = r"quotes_6_68_25-10-2023_output.xlsx"
    data_file = os.path.join(path, file_name)
    ic(data_file, db_name)

    read_xlsx_to_db(db_name, data_file)
