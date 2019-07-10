from Branch import Branch
from Patch import Patch
from operations import AddFileOperation

def main():

    branch = Branch()
    addOp1 = AddFileOperation("filename", "DATA")
    addOp2 = AddFileOperation("filename", "DATA")
    patch = Patch(set())
    patch.add_operation(addOp1)
    patch.add_operation(addOp2)
    branch.add_patch(patch)
    print(branch.states[-1].files)

main()