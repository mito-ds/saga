import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="saga-vcs",
    version="0.0.9",
    author="saga",
    author_email="narush@wharton.upenn.edu.com",
    description="saga is a version control CLI that handles many file formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/naterush/saga",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
     entry_points={
        'console_scripts': [
            'saga = saga.main:main'
        ]
    },
    python_requires='>=3.6',
)