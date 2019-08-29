# saga

## Instructions

### Requirments

Make sure git, python3, pip and virtualenv are installed on your computer. 

### Setup

To download and setup the software:

~~~~
git clone https://github.com/naterush/version-control.git;
cd version-control;
virtualenv venv;
source venv/bin/activate;
pip install -r requirements.txt;
~~~~

### Using saga

Coming soon!

### Running Tests

When inside of the python virtual enviorment:
~~~~
python -m pytest
~~~~


## SPECIFICATION

We assume that we have a set of files Files. These files may have different formats and different structure; they may be text files, they may be audio files, etc. Let us call all these formats Formats.

For any file of any type, we have a number of operations that can be performed on them:
- add file
- delete file

Then, for each file with a type format, we may define additional operations that can be performed on these files. For example, for a text file:
- add line
- remove line
- modify line

or for an audio file:
- add track
- etc.

------

Now, armed with these operations on files, we can consider a patch to be any list of these operations. A valid patch is defined by the operations included in it. Each operation can restrict what other operations it can be in a patch with (e.g. a remove operation may not be allowed with a modify file operation). TODO: this is outdated.

We then define a branch to be any list of valid patches. For a branch to be valid, each patch on the branch must be valid; furthermore, there must be consistency between patches in the branch. For a file to be created, it must not already exist. For a file to be deleted, it must exist. 

Consider a branch made up of patches P1, P2, P3, ..., Pn. We can consider the state "i" of the branch to be the result of the files after applying pathces P1, ... Pi. State 0 is the empty set. Furthermore, the state is just represented as a map from ID -> file contents (e.g. ID's are unique).

Patch Pi can only give it's validity conditions based on state i - 1. Furthermore, any patch must define it's "area of effect." This is the files that it's validity conditions apply to.

Finially, we define a repository to be any set of branches.


-------

How do we move from LCS calculation to figuring out what changes were made (for now, just a text file)?

We can think of the indexes as a map:

a b c d e f g h
|  \   /      
a k b e z z z z

If a line from the old file has no matches, than it was deleted. If a line from the new file has no matches, than it was added. We can first calculate the removed lines by looping over the all lines in the file and marking the ones that don't have matches. In the above file, this would result in:

a b e
|  \ \ 
a k b e z z z z 

Then, we can loop over the new file, and keep track of all the lines that have been added (and what they have been added as).