# saga

saga is a set of tools for version control. As a user, you can use 

As a developer, you can use saga's framework to add intelligent version control to any software project. Simply tell saga what your file looks like, and saga will auto-magically allow git-level branching, patching, and merging. Oh gee, think of the collaboration possible!

## Installation Instructions

To install the `saga` command line tool, run:

~~~~
pip install saga-vcs
~~~~

Currently, saga only works on macOS. Support for Linux and Windows is coming soon!

## Using saga

Currently, the `saga` command line tool has a very similar interface to git. The following commands are currently supported:

~~~~
saga init
saga add 
saga commit
saga log
saga status
saga branch
saga checkout
saga merge
~~~~

Some commands don't perform exactly as git does, so watch out! 

## Warning

Saga is pre-alpha software. Do not use saga to manage any files that you don't totally trust (we are sure there are security vulnerabilities hanging about). 

## Downloading Saga Source

If you want to check out saga's source code (or contribute <3):

~~~~
git clone https://github.com/naterush/version-control.git;
cd version-control;
python3 -m venv env;
source env/bin/activate;
pip install -r requirements.txt;
~~~~

### Running Tests

When inside of the python virtual enviorment:
~~~~
python -m pytest
~~~~
