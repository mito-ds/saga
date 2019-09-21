from saga.file_types.excel_file import parse_excel_file, write_excel_file
from bs4 import BeautifulSoup
from zipfile import ZipFile

NO_VALUE = "NO_VAL_HERE"

def char_position(letter):
    return ord(letter) - 97

with ZipFile("temp/excel.xlsx", 'r') as zf:
    # first, we will build the shared strings map
    with zf.open('xl/sharedStrings.xml') as myfile:
        soup = BeautifulSoup(myfile.read(), 'html5lib')
        unique_strs =  [None] * int(soup.body.sst["count"])
        for i, val in enumerate(soup.body.sst):
            unique_strs[i] = val.contents[0].contents[0]
        print(unique_strs)

    with zf.open('xl/worksheets/sheet1.xml') as myfile:
        soup = BeautifulSoup(myfile.read(), 'html5lib')

        for row in soup.html.body.worksheet.dimension.sheetformatpr.sheetdata:
            span = row["spans"].split(":")
            start = int(span[0])
            end = int(span[1])
            parsed_row = [None] * end 
            for cell in row:
                cell_name = cell["r"]
                column = "".join([c for c in cell_name if c.isalpha()])
                
                is_string = "t" in cell.attrs
                is_formula = len(cell.contents) > 1

                print(cell_name, cell, "str: {}, form: {}".format(is_string, is_formula))
                print(column)

            print(start, end)
