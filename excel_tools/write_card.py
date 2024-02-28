import sqlite3
from icecream import ic
import re
from excel_tools.config_data import Quote, Attribute, Option


def get_quote_cards_from_db(db_file_name: str) -> list[Quote]:
    def regex(expression, item):
        reg = re.compile(expression)
        return reg.search(item) is not None

    quote_storage: list[Quote] = []
    # 'Quote' 'Attributes' 'Options'
    query_get_attributes = """SELECT a.ATTRIBUTE_TITLE, a.VALUE FROM Attributes a WHERE a.PRESSMARK = ?;"""
    query_get_options = """SELECT * FROM Options o WHERE o.PRESSMARK = ?;"""

    connection = sqlite3.connect(db_file_name, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.create_function("REGEXP", 2, regex)

    cursor = connection.execute(f"SELECT * FROM Quote;")
    for row in cursor.fetchall(): #[:2]
        # ic(row['GROUP_WORK_PROCESS'], row['PRESSMARK'], row['TITLE'][:20], row['UNIT_OF_MEASURE'])
        # ic(row.keys())
        quote = Quote(
            table=row['GROUP_WORK_PROCESS'],
            code=row['PRESSMARK'],
            title=row['TITLE'],
            measure=row['UNIT_OF_MEASURE'],
            type_quote=row['SUPPLEMENTARY_TYPE'],
            parent_quote=row['PARENT_PRESSMARK']
        )
        attr_cursor = connection.execute(query_get_attributes, (row['PRESSMARK'], ) )
        for attr in attr_cursor.fetchall():
            quote.attributes.append(Attribute(name=attr['ATTRIBUTE_TITLE'], value=attr['VALUE']))

        opt_cursor = connection.execute(query_get_options, (row['PRESSMARK'],))
        for opt in opt_cursor.fetchall():
            option = Option(
                name=opt['PARAMETER_TITLE'], left=opt['LEFT_BORDER'], right=opt['RIGHT_BORDER'],
                unit_measure=opt['UNIT_OF_MEASURE'], step=opt['STEP'], option_type=opt['PARAMETER_TYPE']
            )
            quote.options.append(option)
        quote_storage.append(quote)
    connection.close()
    return quote_storage


def get_resource_cards_from_db(db_file_name: str) -> list[Quote]:
    def regex(expression, item):
        reg = re.compile(expression)
        return reg.search(item) is not None

    quote_storage: list[Quote] = []
    # 'Resources', 'Attributes', 'Options'
    query_get_attributes = """SELECT a.ATTRIBUTE_TITLE, a.VALUE FROM Attributes a WHERE a.PRESSMARK = ?;"""
    query_get_options = """SELECT * FROM Options o WHERE o.PRESSMARK = ?;"""

    connection = sqlite3.connect(db_file_name, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.create_function("REGEXP", 2, regex)

    cursor = connection.execute(f"SELECT * FROM Resources;")
    for row in cursor.fetchall(): #[:2]
        # ic(row['PRESSMARK'], row['TITLE'][:20], row['UOM'])
        # ic(row.keys())
        quote = Quote(
            table="",
            code=row['PRESSMARK'],
            title=row['TITLE'],
            measure=row['UNIT_OF_MEASURE'],
            type_quote='',
            parent_quote=''
        )
        attr_cursor = connection.execute(query_get_attributes, (row['PRESSMARK'], ) )
        for attr in attr_cursor.fetchall():
            quote.attributes.append(Attribute(name=attr['ATTRIBUTE_TITLE'], value=attr['VALUE']))

        opt_cursor = connection.execute(query_get_options, (row['PRESSMARK'],))
        for opt in opt_cursor.fetchall():
            option = Option(
                name=opt['PARAMETER_TITLE'], left=opt['LEFT_BORDER'], right=opt['RIGHT_BORDER'],
                unit_measure=opt['UNIT_OF_MEASURE'], step=opt['STEP'], option_type=opt['PARAMETER_TYPE']
            )
            quote.options.append(option)
        quote_storage.append(quote)
    connection.close()
    return quote_storage


if __name__ == '__main__':
    db_name = r"C:\Users\kazak.ke\Documents\PythonProjects\QuotesReportCard\DB\parameters.sqlite3"
    ic(db_name)

    # quote_data: list[Quote] = get_quote_cards_from_db(db_name)
    quote_data: list[Quote] = get_resource_cards_from_db(db_name)

    ic(quote_data)
    ic(len(quote_data))
