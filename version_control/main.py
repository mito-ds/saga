from version_control.file_types.text_file.TextFile import TextFile


def main():
    text_file1 = TextFile("filename", ["a", "b", "c", "d", "e"])
    text_file2 = TextFile("filename", ["a", "z", "z", "z", "z"])
    text_file1.print_changes(text_file2)

main()