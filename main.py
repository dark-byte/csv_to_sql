import csv
import os
from datetime import datetime
import pandas as pd


def process_csv(file_name):
    df = pd.read_csv(file_name)

    file = "MOCK_DATA"

    clean_tbl_name = file.lower().replace(" ", "_")

    df.columns = [x.lower().replace(" ", "_") for x in df.columns]

    replacements = {
        'object': 'varchar(100)',
        'float64': 'float',
        'int64' : 'int',
        'datetime64': 'timestamp',
        'timestamp64[ns]' : 'varchar'
    }

    col_str = ", ".join("{} {}".format(n, d) for (n, d) in zip(df.columns, df.dtypes.replace(replacements)))

    SQL_STATEMENT = f'CREATE TABLE IF NOT EXISTS {clean_tbl_name} ({col_str});'+'\n'

    insert_template = "INSERT INTO {} ({}) VALUES {};"
    value_template = "({})"

    INSERT_STATEMENT = ""

    def format_value(value, data_type):
        if data_type == 'int':
            return str(value)
        else:
            value = value.replace("'", "")
            return f"'{value}'"

    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames

        values_list = []

        for row in reader:
            values = ', '.join([format_value(row[header], 'int' if row[header].isdigit() else 'str') for header in headers])
            values_list.append(value_template.format(values))

        columns = ', '.join(headers)
        all_values = ', \n'.join(values_list)

        INSERT_STATEMENT = insert_template.format(clean_tbl_name, columns, all_values)


    DATABASE_STATEMENT = f'DROP DATABASE IF EXISTS {clean_tbl_name}_db;\nCREATE DATABASE {clean_tbl_name}_db;\nUSE {clean_tbl_name}_db;\n'
    
    output_file = f'SQL_OUTPUT{str(datetime.now())}.sql'
    with open(os.path.join('static/output', output_file), 'w') as f:
        f.writelines(DATABASE_STATEMENT)
        f.writelines(SQL_STATEMENT)
        f.writelines(INSERT_STATEMENT)
    return output_file
