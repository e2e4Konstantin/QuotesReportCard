import sqlite3
import os
from icecream import ic
import pandas as pd

db_name = r"F:\Temp\python_tests\params.sqlite3"

path = r"F:\Temp\NIAC\output"
file_name = r"quotes_5_67_output.xlsx"
data_file = os.path.join(path, file_name)

ic(data_file)

conn = sqlite3.connect(db_name)
sheets = pd.ExcelFile(data_file).sheet_names
n = 3
ic(sheets[:n])
for sheet in sheets[:n]:
    df = pd.read_excel(data_file, sheet_name=sheet, dtype="object")    # encoding='utf-8' header=None,

    if not df.empty:
        row_max = df.shape[0]-1
        column_max = df.shape[1]-1
        ic(sheet, row_max, column_max)

    conn.execute(f"DROP TABLE IF EXISTS {sheet};")
    df.to_sql(sheet, conn, if_exists='replace', index=False)
    conn.commit()

conn.close()
