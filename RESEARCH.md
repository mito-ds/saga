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

For a given file type F, we have a function get_operations(F, F'), which returns a list of operations (on file F) that get form F to F'.

etc etc

