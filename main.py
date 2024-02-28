import os
from icecream import ic

from excel_tools import read_xlsx_to_db, Quote, get_quote_cards_from_db, write_excel_file, get_resource_cards_from_db


if __name__ == '__main__':

    db_name = r"F:\Kazak\GoogleDrive\Python_projects\QuotesReportCard\DB\parameters.sqlite3"
    path = r"F:\Kazak\GoogleDrive\NIAC\Велесь_Игорь\Файлы к переводу в машиночитаемый вид\output"

    # input_file_name = r"Материалы_1_output_28-02-2024.xlsx"
    input_file_name = r"Расценки_3_68_output_28-02-2024.xlsx"
    # ---------------------------------------------------------->>
    output_file_name = f"Cards_{input_file_name}"
    data_file = os.path.join(path, input_file_name)
    output_file = os.path.join(path, output_file_name)

    ic(data_file, db_name, output_file)
    read_xlsx_to_db(db_name, xlsx_file=data_file)

    # ---> для Расценок ---------------------------------------->>
    quotes_data: list[Quote] = get_quote_cards_from_db(db_name)

    # ---> для Ресурсов ---------------------------------------->>
    # quotes_data: list[Quote] = get_resource_cards_from_db(db_name)

    if len(quotes_data) > 0:
        ic(len(quotes_data))
        write_excel_file(output_file, quotes_data)
    else:
        ic("Файл с карточками не сформирован. Данных нет!")
