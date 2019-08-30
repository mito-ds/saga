# Research

This is a list of open reasearch problems for generalized version control. 

## Longest Common Subsequence with a Change Operation - and a Distance Metric

EDIT: I think it might be this algorithm: https://en.wikipedia.org/wiki/Hirschberg%27s_algorithm, or at least something close!

The longest common subsequence between two strings A= a1, a2, ... an, B=b1, b2, .. bm is a set of characters LCS = l1, l2, ... li where all characters in LCS appear, in order (but not necessarily contigiously) in both A and B, and they are the longest possible sequence that satisfied this constraint. 

This is clearly a useful notion for a version control system; for any list that undergoes changes, the LCS of the old list with the new list can be thought of as the things that do not change. 

However, let us consider in more depth the things that do change. Imagine we have some list:
~~~~
old_list = ["abc", "def", "ghi", "jkl"]
new_list = ["abc", "def", "ghi", "jklm"]
~~~~
With the standard implementation of LCS, we would say that old_list and the new_list differ by a delete on the old list followed by an insert on the new list. 

However, imagine we allowed for "change" operations. Now, clearly, there we can just perform a single change operation to change "jkl" to "jklm." But the this problem quickly becomes intractable. Consider the following list:
~~~~
old_list = ["abc", "def", "ghi", "jkl"]
new_list = ["abc", "HAHAHA", "defi", "ghi", "jkl"]
~~~~
Clearly, the new list has had at least one change and at least one insert as compared to the old list. However, what has occured? Has "def" changed to "HAHAHA" or to "defi"? It seems pretty obvious that it's changed to "defi."

Thus, we are essentially trying to match the list:
~~~~
list1 = ["def"]
list2 = ["HAHAHA", "defi"]
~~~~
That is: given a difference metric between two elements (e.g. some function f(ele1, ele2) -> num), we want to create a matching (ele1, ele2), (ele1', ele2'), ... that maximizes the sum of this function. 

However, in certain cases, we note that there may have just been a delete and an insert performed. That is: pairs should only be formed when the distance metric is above some cutoff...

### Problem Goals
- Given a difference metric, define an efficient algorithm for computing the pairs that have the maximal sum, as mentioned above.
- In the above algorithm, include a "cutoff" value (e.g. pairs can only before formed if they are this close).
- Define a nice metric for strings, JSON objects, etc!
- Do testing to find nice values for these numbers in certain known cases (e.g. with text lines). 

Two notes on the above:
- Github already does this, somehow (e.g. https://github.com/ethereum/eth2.0-specs/pull/1308/files). I suspect when they notice an delete and then insert on the same line, they just find where the lines differ. This is a less robust version of my proposal, I think.
- Github has a bunch of examples we can use to find nice heuristics!



## Give type definitions of version control functions

We note that the following operation are useful, for a given file type F, and two versions of that file:

~~~~
get_operations(file, file') = list of operations to change file to file'
merge_operations(file, file', least_common_ancestor_version) = none if changes cannot be merged, otherwise the operations that can be merged
~~~~

## Give an LCS algorithm for 2D (and more) data

The LCS algorithm takes two lists, and finds the longest common subsequnce between the two lists. For example, in the lists:

~~~~
list1 = [1, 2, 3, 4, 5]
list2 = [0, 1, 0, 2, 0, 3, 0, 4, 0, 5]
~~~~

The LCS would be 1, 2, 3, 4, 5. Clearly, this is useful for version control; we can thus infer that 0's were inserted into the new list. 

How do we think about the LCS algorithm in the context of 2d, or more, data? For example consider a CSV file with the following data:

~~~~
NAME, EMAIL
nate, nate@gmail.com
jim, jim@gmail.com
tim, tim@gmail.com
~~~~

Now, how do we do LCS between this data and another piece of data? A first attempt might be to essentially turn the above into the following list:

~~~~
list = [["NAME", "EMAIL"], ["nate", "nate@gmail.com"], ["jim", "jim@gmail.com"], ["tim", "tim@gmail.com"]]
~~~~

But 



You might just 



For a given file type F, we have a function get_operations(F, F'), which returns a list of operations (on file F) that get form F to F'.

etc etc




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