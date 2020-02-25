import os
import hashlib
import requests
import shutil
from typing import Optional, List
from pathlib import Path
from os.path import join
from saga.Commit import Commit
from saga.path_utils import (
    copy_dir_to_dir,
    relative_paths_in_dir,
    changed_files
)
from saga.file_types.file_utils import parse_file


class Repository(object):

    def __init__(self, directory: Path):
        self.base_directory = directory

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
        return [
            str(path.parts[-1]) for path in self.branch_directory.iterdir()
        ]

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
                # we encode the file contents
                # and we encode the file path
                m.update(file_bytes)
                m.update(file_name.encode("utf-8"))
                file_hashes.append(m.hexdigest())
        m = hashlib.sha256()
        # TODO: this should be a merkle tree eventually
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
                f.write("http://localhost:3000")
            return "http://localhost:3000"

    def head_commit_from_branch(self, branch_name: str) -> Optional[str]:
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
    def curr_state_directory(self) -> Path:
        """
        Returns the path with of the head state directory
        """
        return self.state_directory / self.state_hash

    

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
        inserted, changed, removed = changed_files(
            ".",
            join(".saga/states", state_hash)
        )
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

    def get_state_hash(self, branch):
        commit_hash = self.head_commit_from_branch(branch)
        commit = self.get_commit(commit_hash)
        return commit.state_hash
