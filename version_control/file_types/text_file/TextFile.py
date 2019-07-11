from version_control.file_types.file.File import File

class TextFile(File):

    # A text file is a map from line number to text data
    # it's an array of strings, tbh; just bump everything up when you need to
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def change_line(self, line_number, line_contents):
        if line_number >= len(self.file_contents):
            raise Exception("cannot change line that is greater than contents")
        self.file_contents[line_number] = line_contents

    def insert_line(self, line_number, line_contents):
        if line_number >= len(self.file_contents):
            raise Exception("cannot change line that is greater than contents")
        self.file_contents.insert(line_number, line_contents)

    def append_line(self, line_contents):
        self.file_contents.push(line_contents)