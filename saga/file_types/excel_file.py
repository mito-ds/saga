from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile
from math import isnan

def filter_nan(values):
    for row_idx, row in enumerate(values):
        to_delete = []
        for idx, val in enumerate(row):
            if isinstance(val, float) and isnan(val):
                to_delete.append(idx)

        for idx in reversed(to_delete):
            del row[idx]

        values[row_idx] = row

    return values


def parse_excel_file(file_id, file_name, file_path):
    xl = pd.ExcelFile(file_path)
    df = xl.parse('Sheet1', convert_float=False)

    columns = df.columns
    values = filter_nan(df.values.tolist())
    values.insert(0, [val for val in columns if type(val) == str and not val.startswith("Unnamed:")])
    print("{}: {}".format(file_path, values))

    l = MultiDimList(values, 2)
    return File(file_id, "excel", file_name, l)
    
    """
    sheets = []
    for idx, sheet_name in enumerate(xl.sheet_names):
        df1 = xl.parse('Sheet1')
    """

def write_excel_file(file):
    df = DataFrame.from_records(file.file_contents.multi_dim_list)
    print(df)
    writer = pd.ExcelWriter(file.file_name, engine='xlsxwriter', )
    df.to_excel(writer, 'Sheet1', index=False, header=False) #index=false says don't write the row indices 
    writer.save()

