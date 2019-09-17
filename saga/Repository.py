import os
import pickle
import shutil
import hashlib
import copy
import filecmp
import glob
from os.path import join, isfile
from saga.Commit import Commit
from saga.file_types.file_utils import parse_file, write_file

class Repository(object):

    def __init__(self, directory):
        self.base_directory = directory
        self.saga_directory = self.base_directory + "/.saga/"
        self.commit_directory = self.base_directory + "/.saga/commits/"
        self.state_directory = self.base_directory + "/.saga/states/"
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
        repo = Repository(directory)
        repo.commit("Create repository") # we add this empty commit so we don't need special cases
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
        f = open(self.repo_pickle, "wb+")
        p = pickle.dumps(self)
        f.write(p)
        f.close()

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
        for file_path in sorted([f for f in self.index[self.head]]):
            if os.path.exists(file_path):
                f = open(file_path, "rb")
                file_bytes = f.read()
                m = hashlib.sha256()
                m.update(file_bytes)
                file_hashes.append(m.hexdigest())
            else:
                self.index[self.head].remove(file_path) # we don't keep around dead files anymore
        m = hashlib.sha256()
        #TODO: this should be a merkle tree eventually 
        # (or maybe an merkel-mountain-range), to reap the benefits
        m.update(",".join(file_hashes).encode('utf-8')) 
        return m.hexdigest()

    def get_new_file_id(self):
        # generates a random ID for a file
        import uuid
        return uuid.uuid4().hex

    def add(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                # if it's a directory, we recursively think about all the files below it
                for f in [join(path, f) for f in os.listdir(path) if isfile(join(path, f))]:
                    self.index[self.head].add(f)
            else:
                self.index[self.head].add(path)
        else:
            print("Error: path {} does not exist".format(path))

    def commit(self, commit_message):
        state_hash = self.index_hash()
        parent_commit_hash = self.branches[self.head]
        commit = Commit(state_hash, [parent_commit_hash], commit_message)
        commit_hash = self._add_commit_to_db(commit)
        self.commits[self.head].append(commit_hash)
        self._backup_state_to_db()
        # we need to add a save state 

        self.branches[self.head] = commit_hash

    def create_branch(self, branch_name):
        if branch_name in self.branches:
            print("Error: branch {} already exists".format(branch_name))
        self.branches[branch_name] = self.branches[self.head]
        self.index[branch_name] = copy.deepcopy(self.index[self.head])
        self.file_ids[branch_name] = copy.deepcopy(self.file_ids[self.head])
        self.commits[branch_name] = copy.deepcopy(self.commits[self.head])

    def switch_to_branch(self, branch_name):
        if branch_name not in self.branches:
            print("Error: cannot switch to branch {} as it does not exist".format(branch_name))
            return

        self.head = branch_name
        commit = self.get_commit(self.branches[self.head])
        self._restore_state(commit.state_hash)

    def _paths_in_dir(self, directory, ignore=None):    
        if ignore is None:
            ignore = []

        prefix = len(directory)
        paths = [path[prefix + 1:] for path in glob.glob(directory + '/**', recursive=True) if path[prefix + 1:] != ""]
        def include_path(path):
            for ignore_path in ignore:
                if path.startswith(ignore_path):
                    return False
            if path == directory:
                return False
            return True
        return {path for path in paths if include_path(path)}

    def state_hash(self):
        return self.get_commit(self.branches[self.head]).state_hash

    def changed_files(self, dir1, dir2):
        previous_state = self._paths_in_dir(dir1)
        current_state = self._paths_in_dir(dir2)

        removed_paths, changed_paths, inserted_paths  = set(), set(), set()
        for path in previous_state:
            if path not in current_state:
                removed_paths.add(path)
            elif not filecmp.cmp(join(dir1, path), join(dir2, path)):
                changed_paths.add(path)
        for path in current_state:
            if path not in previous_state:
                inserted_paths.add(path)

        return removed_paths, changed_paths, inserted_paths
        
    def status(self):
        removed_paths, changed_paths, inserted_paths = self.changed_files(join(self.state_directory, self.state_hash()), self.base_directory)
        print("Status:")
        print("\tChanges staged for commit:")
        for path in removed_paths:
            if path in self.index[self.head]:
                print("\t\tremoved: {}".format(path))
        for path in changed_paths:
            if path in self.index[self.head]:
                print("\t\tchanged: {}".format(path))
        for path in inserted_paths:
            if path in self.index[self.head]:
                print("\t\tinserted: {}".format(path))
        
        print("\tChanges not staged for commit:")
        for path in removed_paths:
            if path not in self.index[self.head]:
                print("\t\tremoved: {}".format(path))
        for path in changed_paths:
            if path not in self.index[self.head]:
                print("\t\tchanged: {}".format(path))
        for path in inserted_paths:
            if path not in self.index[self.head]:
                print("\t\tinserted: {}".format(path))


    def get_diff(self):
        _, changed_paths, _ = self.changed_files(join(self.state_directory, self.state_hash()), self.base_directory)

        print("Git diff:")
        operations = []
        for path in changed_paths:
            if path in self.index[self.head]:
                print("\tFile:", path)
                # we should read in the current file and the old file in this case
                file_id = self.file_ids[self.head][path]
                old_file = parse_file(file_id, path, join(self.state_directory, self.state_hash(), path))
                new_file = parse_file(file_id, path, join(self.base_directory, path))
                ops = old_file.get_operations(new_file)
                for op in ops:
                    print("\t\t:", op)
                operations.extend(ops)

        return operations

    def merge(self, other_branch):
        if other_branch not in self.branches:
            print("Error: cannot merge branch {} as it does not exist".format(other_branch))

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

            removed_paths_A, changed_paths_A, inserted_paths_A = self.changed_files(state_dir_old, state_dir_newA)
            removed_paths_B, changed_paths_B, inserted_paths_B = self.changed_files(state_dir_old, state_dir_newB)

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

    def _backup_state_to_db(self):
        # copies all files that are being tracked to the
        dst = self.state_directory + self.index_hash() 
        if not os.path.exists(dst):
            os.mkdir(dst)
            for file_name in self.index[self.head]:
                # make new directories if we need to 
                if isfile(file_name):
                    if file_name not in self.file_ids[self.head]:
                        self.file_ids[self.head][file_name] = self.get_new_file_id()
                    # we need to make directories down to this one
                    directory = "/".join(file_name.split("/")[:-1])
                    if not os.path.exists(dst + "/" + directory):
                        os.mkdir(dst + "/" + directory)
                    shutil.copyfile(file_name, dst + "/" + file_name)
                else:
                    # must be a directory, and so we can just make the directory
                    if not os.path.exists(dst + "/" + file_name):
                        os.mkdir(dst + "/" + file_name)


    def _restore_state(self, state_hash):

        for root, dirs, files in os.walk(self.state_directory + state_hash):
            local_path = root.split(self.state_directory)[1][65:]
            for directory in dirs:
                # if the directory doesn't exist, we make it
                path = join(local_path, directory)
                if not os.path.isdir(join(self.base_directory, path)):
                    os.mkdir(join(self.base_directory, path))

            for file_name in files:
                path = join(local_path, file_name)
                shutil.copyfile(join(self.state_directory, state_hash, path), join(self.base_directory, path))

