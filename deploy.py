import os
import shutil
import time

# We delete the last deployment folders, if they exist
DEPLOYMENT_FOLDERS = ["build", "dist", "saga_vcs.egg-info"]

for folder in DEPLOYMENT_FOLDERS:
    if os.path.exists(folder):
        shutil.rmtree(folder)

# Then, we ask for a new version number
version_string = input("What version is this? ")

# write out the version number, to be read in by the setup script
f = open("versionnumber", "w+")
f.write(version_string)
f.close()

# Finially, we make setup the distribution to upload
os.system("python3 setup.py sdist bdist_wheel")

# delete the stored version number
os.remove("versionnumber")

# Finially, we upload this to PyPi
os.system("twine upload dist/*")

# Then, we delete the folders again, cuz we don't need them anymore
for folder in DEPLOYMENT_FOLDERS:
    if os.path.exists(folder):
        shutil.rmtree(folder)