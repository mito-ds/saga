from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile

def parse_excel_file(file_id, file_name, file_path):
    df = pd.read_excel(file_path, sheetname='Sheet1')
    l = MultiDimList(df.tolist(), 2)
    return File(file_id, "excel", file_name, l)

def write_excel_file(self, file):
    df = DataFrame.from_records(file.file_contents.multi_dim_list)
    writer = ExcelWriter(file.file_name)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

