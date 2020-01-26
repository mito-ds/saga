import os
import pickle
import hashlib
import copy
import filecmp
import glob
import requests 
import os
import glob
import json
import shutil
from typing import Optional, List
from pathlib import Path
from os.path import join, isfile
from saga.Commit import Commit
from saga.path_utils import copy_dir_to_dir, copy_file_to_dir, relative_paths_in_dir, changed_files
from saga.file_types.file_utils import parse_file, write_file



class Repository1(object):

    def __init__(self, directory: Path):
        self.base_directory = directory
        self.file_ids = {"master": dict()} # map from branch -> file_name -> permanent_file_id
        self.commits = {"master": []} # this is an ugly hack for now, but we keep track of commit hashes on any branch

    def debug(self):
        for branch in self.branches:
            commit_hash = self.head_commit_from_branch(branch)
            string = ""
            while commit_hash:
                string = f"{commit_hash} - {string}"
                commit = self.get_commit(commit_hash)
                if commit is None or not any(commit.parent_commit_hashes):
                    commit_hash = None
                else:
                    commit_hash = commit.parent_commit_hashes[0]
            print(f"{branch}: {string}")

    @property
    def saga_directory(self) -> Path:
        # TODO: move all of these to paths
        return self.base_directory / ".saga/"

    @property
    def commit_directory(self) -> Path:
        return self.saga_directory / "commits"

    @property
    def state_directory(self) -> Path:
        return self.saga_directory / "states"

    @property
    def index_directory(self) -> Path:
        return self.saga_directory / "index"

    @property
    def branch_directory(self) -> Path:
        return self.saga_directory / "branches"

    @property
    def branches(self) -> List[str]:
        return [str(path.parts[-1]) for path in self.branch_directory.iterdir()]

    @property
    def head_location(self) -> Path:
        return self.saga_directory / "head"

    @property
    def remote_location(self) -> Path:
        return self.saga_directory / "remote"

    @property
    def head(self) -> str:
        if self.head_location.exists():
            with open(self.head_location, "r") as f:
                return f.readline()
        else:
            with open(self.head_location, "w+") as f:
                f.write("master")
            return "master"

    @property
    def index_hash(self):
        """
        Returns the hash of a list of the files + contents, currently
        in the index folder.
        """
        file_hashes = []
        # we sort to have the same files every time
        for file_name in sorted(relative_paths_in_dir(self.index_directory)):
            index_file_name = join(self.index_directory, file_name)
            if os.path.isfile(index_file_name):
                f = open(index_file_name, "rb")
                file_bytes = f.read()
                m = hashlib.sha256()
                m.update(file_bytes) # we encode the file contents
                m.update(file_name.encode("utf-8")) # and we encode the file path
                file_hashes.append(m.hexdigest())
        m = hashlib.sha256()
        #TODO: this should be a merkle tree eventually 
        # (or maybe an merkel-mountain-range), to reap the benefits
        m.update(",".join(file_hashes).encode('utf-8')) 
        return m.hexdigest()

    @property
    def head_commit_hash(self):
        """
        Returns the commit hash on HEAD
        """
        return self.head_commit_from_branch(self.head)

    @property
    def remote_repository(self):
        """
        Returns the URL of the currently tracked remote repository
        """
        if self.remote_location.exists():
            with open(self.remote_location, "r") as f:
                return f.readline()
        else:
            with open(self.remote_location, "w+") as f:
                f.write("None")
            return "None"


    def head_commit_from_branch(self, branch_name: str) -> str:
        branch_file = self.branch_directory / branch_name
        if not branch_file.exists():
            return None
        with open(branch_file, 'r') as f:
            return f.readline()

    @property
    def state_hash(self):
        """
        Returns the state hash of the most recent commit
        """
        head_commit = self.get_commit(self.head_commit_hash)
        return head_commit.state_hash

    @property
    def uncommited_in_index(self):
        index_state_hash = self.index_hash
        commit_state_hash = self.state_hash
        return index_state_hash != commit_state_hash

    def get_commit(self, commit_hash: str) -> Optional[Commit]:
        with (self.commit_directory / commit_hash).open("rb") as f:
            return Commit.from_bytes(f.read())
        return None
        
    def add_commit(
            self, 
            state_hash: str, 
            previous_commit_hashes: List[str],
            commit_message: str
        ) -> Optional[Commit]:
        """
        Adds a commit to the head branch
        """
        commit = Commit(state_hash, previous_commit_hashes, commit_message)
        commit_hash = commit.hash
        commit_bytes = commit.to_bytes()
        with open(self.commit_directory / commit_hash, "wb+") as f:
            f.write(commit_bytes)
        return commit

    def update_head_commit(self, commit: Commit):
        head = self.branch_directory / self.head
        with open(head, "w") as f:
            f.write(commit.hash)

    def set_head(self, branch_name: str):
        with open(self.head_location, "w") as f:
            f.write(branch_name)

    def restore_state(self, state_hash: str):
        # copy the state directory to the current directory
        copy_dir_to_dir(join(".saga/states", state_hash), ".")
        # remove all the files that shouldn't be in this state
        inserted, changed, removed = changed_files(".", join(".saga/states", state_hash))
        for path in inserted:
            if os.path.isdir(path):
                os.rmdir(path)
            else:
                os.remove(path)
        # make the index the proper state
        shutil.rmtree(self.index_directory)
        os.mkdir(self.index_directory)
        copy_dir_to_dir(join(".saga/states", state_hash), self.index_directory)

    def set_remote(self, remote_repository):
        with self.remote_location.open("w+") as f:
            f.write(remote_repository)
        print(f"Set new remote repository to {self.remote_repository}")

    def commit(self, commit_message, allowed_empty=False):
        """
        Creates a new commit with commit_message, if there are new changes to commit
        """
        state_hash = self.index_hash()
        parent_commit_hash = self.branches[self.head]

        if not allowed_empty and not self._uncommited_in_index():
            print("Error: no changes to commit")
            return

        commit = Commit(state_hash, [parent_commit_hash], commit_message)
        commit_hash = self._add_commit_to_db(commit)
        print("[{}] {}".format(commit_hash[0:12], commit_message))
        self.commits[self.head].append(commit_hash)
        self._backup_index_to_db()
        self.branches[self.head] = commit_hash

    def create_branch(self, branch_name):
        """
        If branch_name does not exist, will create a new branch with this name, 
        branching off from the current commit on head
        """
        if branch_name in self.branches:
            print("Error: branch {} already exists".format(branch_name))
        self.branches[branch_name] = self.branches[self.head]
        self.index[branch_name] = copy.deepcopy(self.index[self.head])
        self.file_ids[branch_name] = copy.deepcopy(self.file_ids[self.head])
        self.commits[branch_name] = copy.deepcopy(self.commits[self.head])

    def switch_to_branch(self, branch_name):
        """
        Switches the current head to branch name. Will fail if there are uncommited
        or unstaged changes (that aren't inserts).
        """
        if branch_name not in self.branches:
            print("Error: cannot switch to branch {} as it does not exist".format(branch_name))
            return

        if self._uncommited_in_index():
            print("Error: cannot switch branch as there are uncommited changed")
            return

        inserted, changed, removed = changed_files(self.base_directory, self.curr_state_dir())
        if any(changed) or any(removed):
            print("Error: please commit or undo changes before switching branches")
            return

        print("Switching to branch {}".format(branch_name))
        self.head = branch_name
        commit = self.get_commit(self.branches[self.head])        
        self._restore_state(commit.state_hash)

    def log(self):
        """
        Prints all commits in the current branch to the screen
        """
        for commit_hash in reversed(self.commits[self.head]):
            commit = self.get_commit(commit_hash)
            print("commit: {}".format(commit_hash))
            print("\t{}\n".format(commit.commit_message))
        
    def status(self):
        """
        Prints the status of the current branch and index
        """
        print("On branch {}".format(self.head))

        rem_state_to_index, cha_state_to_index, ins_state_to_index = changed_files(self.curr_state_dir(), self.index_directory)
        rem_index_to_curr, cha_index_to_curr, ins_index_to_curr = changed_files(self.index_directory, self.base_directory)

        print("Changes staged for commit:")
        for path in rem_state_to_index:
            print("\tremoved: {}".format(path))
        for path in ins_state_to_index:
            print("\tinserted: {}".format(path))
        for path in cha_state_to_index:
            if path not in cha_index_to_curr and path not in rem_index_to_curr:
                print("\tmodified: {}".format(path))

        print("Change not staged for commit:")
        for path in rem_index_to_curr:
            print("\tremoved: {}".format(path))
        for path in cha_index_to_curr:
            print("\tmodified: {}".format(path))

        print("Untracked files:")
        for path in ins_index_to_curr:
            print("\t{}".format(path))

    def diff(self):
        """
        Prints the differences between all files
        """
        _, changed_paths, _ = changed_files(self.index_directory, self.base_directory)

        print("Git diff:")
        operations = []
        for path in changed_paths:
            if os.path.isfile(path):
                print("\tFile:", path)
                # we should read in the current file and the old file in this case
                file_id = self.file_ids[self.head][path]
                old_file = parse_file(file_id, path, join(self.index_directory, path))
                new_file = parse_file(file_id, path, join(self.base_directory, path))
                ops = old_file.get_operations(new_file)
                for key in ops:
                    print("\t\t:", key, ops[key])
                operations.extend(ops)
            else:
                print("\tDirectory:", path, "changed")

        return operations


    def pull(self):
        URL = f"{self.remote_repository}/cli/get-folder"

        shutil.rmtree(self.saga_directory)

        try:
            response = requests.get(url = URL, data={'folder_location' : ".saga"})
            paths = response.json()

            # create all the folders we need
            for path in paths["folder_paths"]:
                os.makedirs(os.path.join(self.base_directory, path))

            # and then download all the files in these folders
            for path in paths["file_paths"]:
                self._pull_file(path)
        except:
            print("Error: cannot pull")

    def push(self):
        relative_paths = relative_paths_in_dir(".saga")

        for path in relative_paths:
            abs_path = os.path.join(".saga", path)
            if os.path.isfile(abs_path):
                # Found a file 
                self._push_file(abs_path)
            else:
                self._push_folder(abs_path)

    def _pull_file(self, relative_file_path):
        # api-endpoint 
        URL = f"{self.remote_repository}/cli/download"

        # sending get request and saving the response as response object 
        r = requests.get(url = URL, data={'file_location' : relative_file_path})

        f = open(relative_file_path,'wb+')
        f.write(r.content)
        f.close()
        print("Downloaded File: {}".format(relative_file_path))

    def _push_file(self, relative_file_path):
        # api-endpoint 
        URL = f"{self.remote_repository}/cli/single-upload"

        file_name = os.path.basename(relative_file_path)

        with open(relative_file_path, 'rb') as f:
            r = requests.post(URL, files={"file": f}, data={"relative_file_path": relative_file_path, "file_name": file_name})

    def _push_folder(self, folder_path):
        # api-endpoint 
        URL = f"{self.remote_repository}/cli/push-folder"

        requests.post(url=URL, data={"folder_path": folder_path})

    def curr_state_dir(self):
        return join(self.state_directory, self.get_commit(self.branches[self.head]).state_hash)

    def least_common_ancestor(self, branch_1, branch_2):
        branch_1_commits = self.commits[branch_1]
        branch_2_commits = self.commits[branch_2]

        for i in reversed(range(min(len(branch_1_commits), len(branch_2_commits)))):
            if branch_1_commits[i] == branch_2_commits[i]:
                if i == min(len(branch_1_commits), len(branch_2_commits)) - 1:
                    return branch_1_commits[i], False
                else:
                    return branch_1_commits[i], True 
        
        raise Exception("No common ancestor")

    def _backup_index_to_db(self):
        # copies all files that are being tracked to a state hash directory
        dst = join(self.state_directory, self.index_hash())
        if not os.path.isdir(dst):
            os.mkdir(dst)
            # TODO: make this work when the cwd isn't the base repository
            copy_dir_to_dir(".saga/index/", dst)

    def _add_commit_to_db(self, commit):
        # if the commit exists, we don't need to error
        commit_hash = commit.hash()
        commit_bytes = commit.to_bytes()
        f = open(self.commit_directory + commit_hash, "wb+")
        f.write(commit_bytes)
        f.close()
        return commit_hash

    def get_new_file_id(self):
        # generates a random ID for a file
        import uuid
        return uuid.uuid4().hex

    def _try_create_file_ids(self, file_paths):
        for path in file_paths:
            if path not in self.file_ids[self.head]:
                self.file_ids[self.head][path] = self.get_new_file_id()

    

    def restore_state_to_head(self):
        self._restore_state(self.state_hash())