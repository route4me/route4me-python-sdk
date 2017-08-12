# -*- coding: utf-8 -*-

import os
from setuptools import setup

from route4me.sdk.version import VERSION_STRING


def read(file_name):
    folder = os.path.dirname(__file__)
    fullname = os.path.join(folder, file_name)
    with open(fullname) as f:
        return f.read()


setup(
    name='route4me-sdk',
    version=VERSION_STRING,
    url='https://github.com/route4me/route4me-python-sdk',   # ???
    license='ISC',                                           # ???
    author='Route4Me Python Team',
    author_email='python-team@route4me.com',
    description=('Route4Me Python SDK'),
    long_description=read('README.rst'),
    keywords='route4me, python, sdk, api',                   # ???
    packages=['route4me.sdk', 'route4me.sdk.examples'],      # ???

    # include_package_data=True,
    # zip_safe=False,
    # platforms='any',

    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: SDK',
        'License :: ISC',
        # 'License :: OSI Approved :: BSD License',
        # 'Operating System :: OS Independent',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        # 'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests',

    install_requires=[
        'Werkzeug>=0.9',
        'Jinja2>=2.4',
        'itsdangerous>=0.21',
        'click>=4.0',
    ],
    extras_require={
        'dotenv': ['python-dotenv'],
        'dev': [
            'blinker',
            'python-dotenv',
            'greenlet',
            'pytest>=3',
            'coverage',
            'tox',
            'sphinx',
            'sphinxcontrib-log-cabinet'
        ],
    },
    entry_points='''
        [console_scripts]
        flask=flask.cli:main
    '''

)
