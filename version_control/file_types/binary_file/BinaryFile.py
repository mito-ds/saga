from version_control.file_types.file.File import File

class BinaryFile(File):

    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    # there's not much here, tbh
    def change_contents(self, file_contents):
        self.file_contents = file_contents
