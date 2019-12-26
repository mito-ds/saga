import os
import subprocess
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# we only deploy when the most recent message is a release
commit_message = subprocess.check_output(['git', "log", "-1", "--pretty=%B"]).decode("utf-8")
if not commit_message.startswith("release"):
    print("Error: only deploys on release")
    exit(1)

version = str(commit_message.split(" ")[1]).strip()
print("COMMIT MESSAGE {}".format(commit_message))
print("Uploading version {}".format(version))

setuptools.setup(
    name="saga-vcs",
    version=version,
    author="saga",
    author_email="narush@wharton.upenn.edu.com",
    description="saga is a version control CLI that handles many file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saga-vcs/saga",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        'XlsxWriter>=1.2',
        'beautifulsoup4>=4.8',
        'html5lib>=1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
     entry_points={
        'console_scripts': [
            'saga = saga.main:main'
        ]
    },
    python_requires='>=3.6',
)