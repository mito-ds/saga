# saga

Saga is a version control tool like Git, but it can be used to version control files other than just text. 

As a user, you can use currently use saga to manage your creative projects. Currently, saga includes basic support for unstructed binary files, text files, CSV files, and Excel files.

As a developer, you can use the Saga framework to add version control to new file formats. See examples [here](https://github.com/saga-vcs/saga/blob/master/saga/file_types/text_file.py) and [here](https://github.com/saga-vcs/saga/blob/master/saga/file_types/excel_file.py). Documentation coming soon!

## Installation Instructions

To install the `saga` command line tool, run:

~~~~
pip3 install saga-vcs
~~~~

Currently, Saga only works on macOS. Support for Linux and Windows is coming soon!

## Using saga

Currently, the `saga` command line tool has a very similar interface to Git. The following commands are currently supported:

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

Some commands don't perform exactly as Git does, so watch out! 

## Warning

Saga is pre-alpha software. Do not use saga to manage any files that you don't totally trust (we are sure there are security vulnerabilities hanging about). 

## Downloading Saga Source

If you want to check out saga's source code (or contribute <3):

~~~~
git clone https://github.com/saga-vcs/saga.git;
cd saga;
python3 -m venv env;
source env/bin/activate;
pip install -r requirements.txt;
~~~~

### Running Tests

When inside of the python virtual enviorment:
~~~~
pytest
~~~~

### Profiling a Test

~~~
python3 -m cProfile -m pytest tests/test_excel.py
~~~