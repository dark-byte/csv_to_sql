import numpy as np
import pandas as pd

df = pd.read_csv("MOCK_DATA.csv")

file = "MOCK_DATA"

clean_tbl_name = file.lower().replace(" ", "_")

df.columns = [x.lower().replace(" ", "_") for x in df.columns]

replacements = {
    'object': 'varchar',
    'float64': 'float',
    'int64' : 'int',
    'datetime64': 'timestamp',
    'timestamp64[ns]' : 'varchar'
}

col_str = ", ".join("{} {}".format(n, d) for (n, d) in zip(df.columns, df.dtypes.replace(replacements)))
print(col_str)