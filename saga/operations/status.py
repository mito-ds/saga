from saga.Repository import Repository
from saga.path_utils import changed_files

def status(repository: Repository):
        """
        Prints the status of the current branch and index
        """
        print("On branch {}".format(repository.head))

        rem_state_to_idx, cha_state_to_idx, ins_state_to_idx = changed_files(
            repository.curr_state_directory,
            repository.index_directory
        )
        rem_index_to_cur, cha_index_to_cur, ins_index_to_cur = changed_files(
            repository.index_directory,
            repository.base_directory
        )

        print("Changes staged for commit:")
        for path in rem_state_to_idx:
            print(f"\tremoved: {path}")
        for path in ins_state_to_idx:
            print(f"\tinserted: {path}")
        for path in cha_state_to_idx:
            if path not in cha_index_to_cur and path not in rem_index_to_cur:
                print(f"\tmodified: {path}")

        print("Change not staged for commit:")
        for path in rem_index_to_cur:
            print(f"\tremoved: {path}")
        for path in cha_index_to_cur:
            print(f"\tmodified: {path}")

        print("Untracked files:")
        for path in ins_index_to_cur:
            print(f"\t{path}")