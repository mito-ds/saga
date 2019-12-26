from saga.base_file.File import File
from bs4 import BeautifulSoup
from zipfile import ZipFile

def char_position(letter):
    return ord(letter) - 65

def get_index(column):
    # for now, we're only gonna do single letter columns
    return char_position(column)

def get_strings(zf):
    try:
        with zf.open('xl/sharedStrings.xml') as stringFile:
            soup = BeautifulSoup(stringFile.read(), 'html5lib')
            unique_strs =  [None] * int(soup.body.sst["count"])
            for i, val in enumerate(soup.body.sst):
                unique_strs[i] = str(val.contents[0].contents[0])
        return unique_strs
    except:
        return []

def get_rows(sheetdata, strings):
    rows = dict()

    # we check if the sheet is empty
    if len(sheetdata) < 1:
        return rows

    rows = dict()
    row_idx = None
    for row in sheetdata:
        try:
            span = row["spans"].split(":")
        except:
            print(row)
            if row_idx is None:
                continue
            rows[row_idx] = []
            continue
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
                string = strings[idx]
                parsed_row[column] = string
            elif is_formula:
                formula = "=" + cell.contents[0].contents[0]
                parsed_row[column] = formula
            else:
                try:
                    val = int(cell.contents[0].contents[0])
                except:
                    val = float(cell.contents[0].contents[0])
                parsed_row[column] = val

        rows[row_idx] = parsed_row

    return rows

def get_cells(zf, strings):
    with zf.open('xl/worksheets/sheet1.xml') as myfile:
        soup = BeautifulSoup(myfile.read(), 'html5lib')
        sheetdata = soup.html.body.worksheet.dimension.sheetformatpr.sheetdata

        rows = get_rows(sheetdata, strings)

        if not any(rows):
            return []
        
        max_row = max(rows) 
        mdl = [[]] *  max_row
        for row in rows:
            mdl[row - 1] = rows[row]
            
    return mdl

def parse_excel_file(file_id, file_name, file_path):

    with ZipFile(file_path, 'r') as zf:
        # first we build the strings map
        strings = get_strings(zf)

        # then, we build the cells map
        cells = get_cells(zf, strings)

    return File(file_id, "excel", file_path, file_name, cells)

def write_excel_file(file):
    import xlsxwriter
    import os

    if os.path.exists(file.file_path):
        os.remove(file.file_path)

    workbook = xlsxwriter.Workbook(file.file_path)
    worksheet = workbook.add_worksheet()
    for row_idx, row in enumerate(file.file_contents.mixed_data_type):
        for col_idx, val in enumerate(row):
            worksheet.write(row_idx, col_idx, val)

    workbook.close()

