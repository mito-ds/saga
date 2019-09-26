from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList

def char_position(letter):
    return ord(letter) - 65

def get_index(column):
    # for now, we're only gonna do single letter columns
    return char_position(column)

def parse_excel_file(file_id, file_name, file_path):
    from bs4 import BeautifulSoup
    from zipfile import ZipFile

    with ZipFile(file_path, 'r') as zf:
        # first, we will build the shared strings map
        with zf.open('xl/sharedStrings.xml') as myfile:
            soup = BeautifulSoup(myfile.read(), 'html5lib')
            unique_strs =  [None] * int(soup.body.sst["count"])
            for i, val in enumerate(soup.body.sst):
                unique_strs[i] = val.contents[0].contents[0]

        with zf.open('xl/worksheets/sheet1.xml') as myfile:
            soup = BeautifulSoup(myfile.read(), 'html5lib')

            rows = dict()
            for row in soup.html.body.worksheet.dimension.sheetformatpr.sheetdata:
                span = row["spans"].split(":")
                start = int(span[0])
                end = int(span[1])
                parsed_row = [None] * end 
                row_idx = None
                for cell in row:
                    cell_name = cell["r"]
                    col_str = "".join([c for c in cell_name if c.isalpha()])
                    row_idx = int(cell_name[len(col_str):])
                    
                    column = get_index(col_str)
                    
                    is_string = "t" in cell.attrs
                    is_formula = len(cell.contents) > 1

                    
                    if is_string:
                        idx = int(cell.contents[0].contents[0])
                        string = unique_strs[idx]
                        parsed_row[column] = string
                    elif is_formula:
                        formula = "=" + cell.contents[0].contents[0]
                        parsed_row[column] = formula
                    else:
                        val = int(cell.contents[0].contents[0])
                        parsed_row[column] = val

                rows[row_idx] = parsed_row
            
            max_row = max(rows) 
            mdl = [[]] *  max_row
            for row in rows:
                mdl[row - 1] = rows[row]
    print(mdl)
    l = MultiDimList(mdl, 2)
    return File(file_id, "excel", file_name, l)

def write_excel_file(file):
    import xlsxwriter
    import os

    if os.path.exists(file.file_name):
        os.remove(file.file_name)

    workbook = xlsxwriter.Workbook(file.file_name)
    worksheet = workbook.add_worksheet()
    for row_idx, row in enumerate(file.file_contents.multi_dim_list):
        for col_idx, val in enumerate(row):
            worksheet.write(row_idx, col_idx, val)

    workbook.close()

