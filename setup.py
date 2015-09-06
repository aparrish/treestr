# chardet's setup.py
from distutils.core import setup
setup(
    name="treestr",
    packages=["treestr"],
    version="0.0.1",
    description="Strings with history and tags",
    author="Allison Parrish",
    author_email="allison@decontextualize.com",
    url="http://github.com/aparrish/treestr",
    download_url="",
    keywords=["strings"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        ],
    long_description="""\
treestr
-------

A string library that remembers things about strings.

Very experimental.

Don't use this for anything.

Requires Python 3 or later.

"""
)
