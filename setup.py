# -*- coding: utf-8 -*-

import os
from setuptools import setup

from route4me.sdk import __release__ as RELEASE
from route4me.sdk import __title__ as TITLE
from route4me.sdk import __copyright__ as COPYRIGHT
from route4me.sdk import __author__ as AUTHOR
from route4me.sdk import __project__ as PROJECT

cwd = os.path.dirname(__file__)


def read_all(file_name):
    fullname = os.path.join(cwd, file_name)
    with open(fullname) as f:
        return f.read()


setup(
    name=TITLE,
    version=RELEASE,
    url='https://github.com/route4me/route4me-python-sdk',
    bugtrack_url='https://github.com/route4me/route4me-python-sdk/issues',
    license='ISC',                                           # ???
    copyright=COPYRIGHT,
    author=AUTHOR,
    author_email='python-team@route4me.com',
    description=PROJECT,
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
    test_suite='pytest',

    install_requires=[
        'six             ==1.10.0',
        'requests        ==2.18.4',
        'enum34          ==1.1.6',
    ],
    # extras_require={
    #     'dev': REQUIREMENTS_DEV,
    # },
    # entry_points='''
    #     [console_scripts]
    #     flask=flask.cli:main
    # '''
)
