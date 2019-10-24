# -*- coding: utf-8 -*-
import os

from setuptools import setup


def read(file_name):
    folder = os.path.dirname(__file__)
    fullname = os.path.join(folder, file_name)
    with open(fullname) as f:
        return f.read()


setup(

    name='route4me-sdk',
    url='https://github.com/route4me/route4me-python-sdk',
    bugtrack_url='https://github.com/route4me/route4me-python-sdk/issues',
    copyright='2016-2019 © Route4Me Python Team',
    author='Route4Me Python Team (SDK)',
    description='Route4Me Python SDK',
    version="0.0.5",
    author_email="juan@route4me.com",
    license="ISC",
    keywords="rout4me, python, sdk, api",
    packages=['route4me'],
    long_description=read('README.md'),
    classifiers=[
        'Environment :: Other Environment',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite="tests",
)
