from saga.file_types.excel_file import parse_excel_file, write_excel_file

val = parse_excel_file("1", "excel.xlsx", "excel.xlsx")
print(val.file_name)
write_excel_file(val)

print(val)