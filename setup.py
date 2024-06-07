# -*- coding: utf-8 -*-
import os

from setuptools import setup
from setuptools import find_packages


from VERSION import PROJECT
from VERSION import COPYRIGHT
from VERSION import AUTHOR
from VERSION import AUTHOR_EMAIL
from VERSION import TITLE
from VERSION import LICENSE
from VERSION import RELEASE_STRING


def read(file_name):
    folder = os.path.dirname(__file__)
    fullname = os.path.join(folder, file_name)
    with open(fullname) as f:
        return f.read()


def rewrite_version():
    with open('VERSION.py', 'r') as inp:
        txt = inp.read()
    outname = os.path.join('route4me', 'version.py')
    with open(outname, 'w') as out:
        out.write(txt)

rewrite_version()


setup(

    name=TITLE,
    url='https://github.com/route4me/route4me-python-sdk',
    bugtrack_url='https://github.com/route4me/route4me-python-sdk/issues',
    copyright=COPYRIGHT,
    author=AUTHOR,
    description=PROJECT,
    version=RELEASE_STRING,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    keywords="rout4me, python, sdk, api",
    packages=find_packages(
        include=['route4me', 'route4me.*'],
        exclude=['*_test*'],
    ),
    zip_safe=True,
    platforms='any',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Environment :: Other Environment',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite="tests",
    install_requires=['six', 'requests'],
)
