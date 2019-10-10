import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

f = open("versionnumber", "r")
versionnumber = f.read()
f.close()

setuptools.setup(
    name="saga-vcs",
    version=versionnumber,
    author="saga",
    author_email="narush@wharton.upenn.edu.com",
    description="saga is a version control CLI that handles many file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saga-vcs/saga",
    packages=setuptools.find_packages(),
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