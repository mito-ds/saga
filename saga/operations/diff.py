from saga.Repository import Repository
from saga.path_utils import changed_files

def diff(repository: Repository):
    """
    Prints the differences between all files
    """
    _, changed_paths, _ = changed_files(
        repository.index_directory,
        repository.base_directory
    )

    print("Saga diff:")
    operations = []
    for path in changed_paths:
        if os.path.isfile(path):
            print("\tFile:", path)
            file_id = 1 # tmp, just for now
            old_file = parse_file(
                file_id,
                path,
                repository.index_directory / path
            )
            new_file = parse_file(
                file_id,
                path,
                repository.base_directory / path
            )
            ops = old_file.get_operations(new_file)
            for key in ops:
                print("\t\t:", key, ops[key])
            operations.extend(ops)
        else:
            print("\tDirectory:", path, "changed")

    return operations

