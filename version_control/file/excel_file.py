from version_control.file.File import File
from version_control.data_types.multi_dim_list.MultiDimList import MultiDimList
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
from pandas import ExcelFile

def parse_csv_file(file_path):
    df = pd.read_excel(file_path, sheetname='Sheet1')
    l = MultiDimList(df.tolist(), 2)
    return File(file_path, "excel", file_path, l)

def write_csv_file(self, file):
    df = DataFrame.from_records(file.file_contents.multi_dim_list)
    writer = ExcelWriter(file.file_name)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

