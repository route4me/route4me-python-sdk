import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Route4Me SDK",
    version = "0.0.1",
    author = "Route4Me",
    author_email = "juan@route4me.com",
    description = ("Route4Me Python SDK"),
    license = "___",
    keywords = "rout4me, python, sdk, api",
    url = "http://route4me.com/api/demo",
    packages=['route4me', 'examples', 'tests', 'docs'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Beta",
        "Topic :: SDK",
        "License :: _____",
    ],
    test_suite="tests",
)
