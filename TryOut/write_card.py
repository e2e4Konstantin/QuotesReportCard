import sqlite3
from icecream import ic
import re
from config_data import Quote, Attribute, Option

quote_data = []

db_name = r"F:\Temp\python_tests\params.sqlite3"
# 'Quote' 'Attributes' 'Options'
query_get_attributes = """SELECT a.ATTRIBUTE_TITLE, a.VALUE FROM Attributes a WHERE a.PRESSMARK = ?;"""
query_get_options = """SELECT * FROM Options o WHERE o.PRESSMARK = ?;"""



def regex(expression, item):
    reg = re.compile(expression)
    return reg.search(item) is not None

conn = sqlite3.connect(db_name, check_same_thread=False)
conn.row_factory = sqlite3.Row
conn.create_function("REGEXP", 2, regex)


cursor = conn.execute(f"SELECT * FROM Quote;")
for row in cursor.fetchall()[:2]: #[:2]
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
    attr_cursor = conn.execute(query_get_attributes, (row['PRESSMARK'], ) )
    for attr in attr_cursor.fetchall():
        quote.attributes.append(Attribute(name=attr['ATTRIBUTE_TITLE'], value=attr['VALUE']))

    opt_cursor = conn.execute(query_get_options, (row['PRESSMARK'],))
    for opt in opt_cursor.fetchall():
        option = Option(
            name=opt['PARAMETER_TITLE'], left=opt['LEFT_BORDER'], right=opt['RIGHT_BORDER'],
            unit_measure=opt['UNIT_OF_MEASURE'], step=opt['STEP'], option_type=opt['PARAMETER_TYPE']
        )
        quote.options.append(option)


    quote_data.append(quote)
conn.close()
print(quote_data)
ic(len(quote_data))
