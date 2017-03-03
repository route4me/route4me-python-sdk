import os
from setuptools import setup

def read(fname):
    folder = os.path.dirname(__file__)
    fullname = os.path.join(folder, fname)
    with open(fullname) as f:
        return f.read()

setup(
    name = "Route4Me SDK",
    version = "0.0.2",
    author = "Route4Me",
    author_email = "juan@route4me.com",
    description = ("Route4Me Python SDK"),
    license = "ISC",
    keywords = "rout4me, python, sdk, api",
    url = "http://route4me.com/api/demo",
    packages=['route4me', 'examples', 'tests', ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Beta",
        "Topic :: SDK",
        "License :: ISC",
    ],
    test_suite="tests",
)
