from version_control.file_types.file.File import File

# TODO: note that having this as a file type is very limiting:
# A user might have this as part of a file, as compared to a file itself. 
# This suggests a new data format: all things are files of different types,
# and the data structure that it is made up of is what these classe are.

class MultiDimList(File):

    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def remove_path(self, path):
        self._remove_path_rec(self.file_contents, path)

    def _remove_path_rec(self, arr, path):
        assert len(path) >= 1

        if len(path) == 1:
            del arr[path[0]]
        elif path[0] == "_":
            for sublist in arr:
                self._remove_path_rec(sublist, path[1:])
        else:
            self._remove_path_rec(arr[path[0]], path[1:])
        
    def insert_path(self, path, value):
        self._insert_path_rec(self.file_contents, path, value) 

    def _insert_path_rec(self, arr, path, value):

        #A = [["A"], ["C"]]
        #B = [["A", "B"], ["C", "D"]]
        # path = ["_", 1]
        # value = ["B", D]


        if len(path) == 1:
            arr.insert(path[0], value[0])
        elif path[0] == "_":
            step = len(value) / len(arr) 
            for idx, sublist in enumerate(arr):
                self._insert_path_rec(sublist, path[1:], value[idx * step: idx * step + step])

        else:
            self._insert_path_rec(arr[path[0]], path[1:], value)
        

    def change_value(self, path, value):
        self._change_value_rec(self.file_contents, path, value)

    def _change_value_rec(self, arr, path, value):
        if len(path) == 1:
            arr[path[0]] = value
        else:
            self._change_value_rec(arr[path[0]], path[1:], value)

    

            



    