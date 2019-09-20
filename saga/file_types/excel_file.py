from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile

def parse_excel_file(file_id, file_name, file_path):
    xl = pd.ExcelFile(file_path)
    df = xl.parse('Sheet1')

    columns = df.columns
    values = df.values.tolist()
    values.insert(0, [val for val in columns])

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

