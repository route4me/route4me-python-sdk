# -*- coding: utf-8 -*-

import os
from setuptools import setup

from route4me.sdk.version import VERSION_STRING


cwd = os.path.dirname(__file__)


def read_all(file_name):
    fullname = os.path.join(cwd, file_name)
    with open(fullname) as f:
        return f.read()


def read_lines(file_name):
    fullname = os.path.join(cwd, file_name)
    with open(fullname) as f:
        return [x.strip() for x in f.readlines()]


REQUIREMENTS = read_lines('requirements.txt')
REQUIREMENTS_DEV = read_lines('requirements-dev.txt')


setup(
    name='route4me-sdk',
    version=VERSION_STRING,
    url='https://github.com/route4me/route4me-python-sdk',   # ???
    license='ISC',                                           # ???
    author='Route4Me Python Team',
    author_email='python-team@route4me.com',
    description=('Route4Me Python SDK'),
    long_description=read_all('README.rst'),
    keywords='route4me, python, sdk, api',                   # ???
    packages=['route4me.sdk', 'route4me.sdk.examples'],      # ???
    platforms='any',

    # include_package_data=True,
    # zip_safe=False,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Environment :: Other Environment',
        'Topic :: SDK',
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='',

    install_requires=REQUIREMENTS,
    extras_require={
        'dev': REQUIREMENTS_DEV,
    },
    # entry_points='''
    #     [console_scripts]
    #     flask=flask.cli:main
    # '''
)
