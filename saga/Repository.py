import os
import pickle
import shutil
from saga.Commit import Commit

class Repository(object):

    def __init__(self, directory):
        self.base_directory = directory
        self.saga_directory = self.base_directory + "/.saga/"
        self.commit_directory = self.base_directory + "/.saga/commits/"
        self.state_directory = self.base_directory + "/.saga/states/"
        self.head = "master"
        self.branches = {} # map from branch name -> commit hash
        self.index = set() # set of all files we are tracking

    @staticmethod
    def init(directory):
        # we make a new .saga repository, if possible
        if os.path.exists(directory + "/.saga"):
            raise ValueError("There is already a saga project at {}".format(directory))
        os.mkdir(cwd + "/.saga")
        os.mkdir(cwd + "/.saga/commits")
        os.mkdir(cwd + "/.saga/states")
        return Repository(directory)

    def get_commit(self, commit_hash):
        try:
            f = open(self.commit_directory + commit_hash, "r")
            commit_string = f.read()
            f.close()
            return Commit.from_string(commit_string)
        except:
            return None

    def _add_commit(self, commit):
        # if the commit exists, we don't need to error
        commit_hash = commit.hash()
        commit_string = commit.to_string()
        f = open(self.commit_directory + commit_hash, "w+")
        f.write(commit_string)
        f.close()

    def head_state(self, )

    def index_hash(self):
        # for now, we just think of the index hash as the path 
        return pickle.dumps()
        for path in self.index:
            if os.path.exists(path):
                if os.path.isdir(path):
                    # if it's a directory, we recursively think about all the files below it

                else:


            else:
                print("FYI, you tracked a deleted path: {}".format(path))

            if 
            # if it's just a file, we just rack it 


    def add(self, path):
        self.index.add(path)

    def commit(self, )

    def get_repos

