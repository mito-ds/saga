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
from os.path import join, isfile
from saga.Commit import Commit
from saga.path_utils import copy_dir_to_dir, copy_file_to_dir, relative_paths_in_dir, changed_files
from saga.file_types.file_utils import parse_file, write_file


class Repository(object):

    def __init__(self, directory):
        self.base_directory = directory
        self.saga_directory = self.base_directory + "/.saga/"
        self.commit_directory = self.base_directory + "/.saga/commits/"
        self.state_directory = self.base_directory + "/.saga/states/"
        self.index_directory = self.base_directory + "/.saga/index/"
        self.repo_pickle = self.base_directory + "/.saga/repository"
        self.head = "master"
        self.branches = {"master" : None} # map from branch name -> commit hash
        self.index = {"master" : set()} # map from branch name -> set of files we are tracking
        self.file_ids = {"master": dict()} # map from branch -> file_name -> permanent_file_id
        self.commits = {"master": []} # this is an ugly hack for now, but we keep track of commit hashes on any branch

    @staticmethod
    def init(directory):
        # we make a new .saga repository, if possible
        if os.path.exists(directory + "/.saga"):
            raise ValueError("There is already a saga project at {}".format(directory))
        os.mkdir(directory + "/.saga")
        os.mkdir(directory + "/.saga/commits")
        os.mkdir(directory + "/.saga/states")
        os.mkdir(directory + "/.saga/index")
        repo = Repository(directory)
        repo.commit("Create repository", is_empty=True) # we add this empty commit so we don't need special cases
        return repo

    @staticmethod
    def read(directory):
        # read from the saga repo pickle
        repo_pickle = directory + "/.saga/repository"
        f = open(repo_pickle, "rb")
        p = f.read()
        f.close()
        return pickle.loads(p)

    def write(self):
        # read from the saga repo pickle
        p = pickle.dumps(self)
        f = open(self.repo_pickle, "wb+")
        f.write(p)
        f.close()

    def add(self, path):
        """
        If a file or folder exists at path, adds to the working index
        """
        if not os.path.exists(path):
            print("Error: path {} does not exist".format(path))
            return

        self._try_create_file_ids([path])

        if os.path.isfile(path):
            copy_file_to_dir(path, self.index_directory)
        else:
            assert os.path.isdir(path)
            files_in_path = relative_paths_in_dir(path)
            # we filter out the saga folder, if need be
            files_in_path = [join(path, f) for f in files_in_path if not f.startswith(".saga")]
            self._try_create_file_ids(files_in_path)
            # copy directory to index
            copy_dir_to_dir(path, join(self.index_directory, path), exclude=[".saga"])

    def commit(self, commit_message, is_empty=False):
        """
        Creates a new commit with commit_message, if there are new changes to commit
        """
        state_hash = self.index_hash()
        parent_commit_hash = self.branches[self.head]

        if not is_empty and not self._uncommited_in_index():
            print("Not commiting: no changes to commit")
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

        _, changed, removed = changed_files(self.base_directory, self.curr_state_dir())
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

    def branch(self):
        """
        Lists the branches in the repo, as well as the head
        """
        for branch in self.branches:
            if branch == self.head:
                print("   * {}".format(branch))
            else:
                print("     {}".format(branch))

    def merge(self, other_branch):
        """
        Merges current head with a other_branch
        """
        if other_branch not in self.branches:
            print("Error: cannot merge branch {} as it does not exist".format(other_branch))
            return


        lca, need_merge = self.least_common_ancestor(self.head, other_branch)

        if not need_merge:
            if len(self.commits[other_branch]) > len(self.commits[self.head]):
                self.branches[self.head] = self.branches[other_branch]
                self.commits[self.head] = copy.deepcopy(self.commits[other_branch])
                commit = self.get_commit(self.branches[self.head])
                self._restore_state(commit.state_hash)
                print("Fast-forward branch {} to branch {}".format(self.head, other_branch))
            else:
                print("Branch {} is a subbranch of {}".format(other_branch, self.head))
        else:

            state_dir_old = join(self.state_directory, self.get_commit(lca).state_hash)
            state_dir_newA = join(self.state_directory, self.state_hash())
            state_dir_newB = join(self.state_directory, self.get_commit(self.branches[other_branch]).state_hash)

            removed_paths_A, changed_paths_A, inserted_paths_A = changed_files(state_dir_old, state_dir_newA)
            removed_paths_B, changed_paths_B, inserted_paths_B = changed_files(state_dir_old, state_dir_newB)

            possibly_mergable = set() 
            print(inserted_paths_A)
            print(inserted_paths_B)
            for path in removed_paths_A.intersection(changed_paths_B):
                print("Confict as {} was removed in {} and modified in {}".format(path, self.head, other_branch))
            for path in removed_paths_B.intersection(changed_paths_A):
                print("Confict as {} was removed in {} and modified in {}".format(path, self.head, other_branch))
            for path in changed_paths_A.intersection(changed_paths_B):
                possibly_mergable.add(path)
                #print("Conflict as {} was modified in both {} and {}".format(path, self.head, other_branch))
            for path in inserted_paths_A.intersection(inserted_paths_B):
                print("Conflict as {} was inserted in both {} and {}".format(path, self.head, other_branch))

            files_to_write = [] # we only write the files if there are no merge conflicts in any of them
            for path in possibly_mergable:
                if path not in self.file_ids[self.head]: # we aren't tracking it
                    continue

                file_id = self.file_ids[self.head][path]
                file_o = parse_file(file_id, path, join(state_dir_old, path))
                file_a = parse_file(file_id, path, join(state_dir_newA, path))
                file_b = parse_file(file_id, path, join(state_dir_newB, path))

                merge_file = file_o.merge(file_a, file_b)
                if merge_file is None:
                    print("Merge conflict for file {}".format(file_o.file_name))
                    return
                else:
                    print("Successfully merged file {}".format(file_o.file_name))
                    files_to_write.append(merge_file)
            for f in files_to_write:
                write_file(f)
            self.commit("Merged {} into branch {}".format(other_branch, self.head))

    def pull(self):
        URL = "http://localhost:3000/cli/get-folder"

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
        URL = "http://localhost:3000/cli/download"

        # sending get request and saving the response as response object 
        r = requests.get(url = URL, data={'file_location' : relative_file_path})

        f = open(relative_file_path,'wb+')
        f.write(r.content)
        f.close()
        print("Downloaded File: {}".format(relative_file_path))

    def _push_file(self, relative_file_path):
        # api-endpoint 
        URL = "http://localhost:3000/cli/single-upload"

        file_name = os.path.basename(relative_file_path)

        with open(relative_file_path, 'rb') as f:
            r = requests.post(URL, files={"file": f}, data={"relative_file_path": relative_file_path, "file_name": file_name})

    def _push_folder(self, folder_path):
        # api-endpoint 
        URL = "http://localhost:3000/cli/push-folder"

        requests.post(url=URL, data={"folder_path": folder_path})

    def state_hash(self):
        return self.get_commit(self.branches[self.head]).state_hash

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

    def _restore_state(self, state_hash):
        copy_dir_to_dir(join(".saga/states", state_hash), ".")
    
    def get_commit(self, commit_hash):
        f = open(self.commit_directory + commit_hash, "rb")
        commit_bytes = f.read()
        f.close()
        return Commit.from_bytes(commit_bytes)

    def _add_commit_to_db(self, commit):
        # if the commit exists, we don't need to error
        commit_hash = commit.hash()
        commit_bytes = commit.to_bytes()
        f = open(self.commit_directory + commit_hash, "wb+")
        f.write(commit_bytes)
        f.close()
        return commit_hash

    def index_hash(self):
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

    def get_new_file_id(self):
        # generates a random ID for a file
        import uuid
        return uuid.uuid4().hex

    def _try_create_file_ids(self, file_paths):
        for path in file_paths:
            if path not in self.file_ids[self.head]:
                self.file_ids[self.head][path] = self.get_new_file_id()

    def _uncommited_in_index(self):
        index_state_hash = self.index_hash()
        commit_state_hash = self.state_hash()
        return index_state_hash != commit_state_hash

    def restore_state_to_head(self):
        self._restore_state(self.state_hash())