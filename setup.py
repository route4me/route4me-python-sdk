# -*- coding: utf-8 -*-

import os
from setuptools import setup
from setuptools import find_packages

from VERSION import PROJECT
from VERSION import COPYRIGHT
from VERSION import AUTHOR
from VERSION import TITLE
from VERSION import LICENSE
from VERSION import RELEASE_STRING

cwd = os.path.dirname(__file__)


def read_all(file_name):
	fullname = os.path.join(cwd, file_name)
	with open(fullname) as f:
		return f.read()


def rewrite_version():
	with open('VERSION.py', 'r') as inp:
		txt = inp.read()
	outname = os.path.join('route4me', 'sdk', 'version.py')
	with open(outname, 'w') as out:
		out.write(txt)


rewrite_version()


setup(
	name=TITLE,
	version=RELEASE_STRING,
	url='https://github.com/route4me/route4me-python-sdk',
	bugtrack_url='https://github.com/route4me/route4me-python-sdk/issues',
	license=LICENSE,
	copyright=COPYRIGHT,
	author=AUTHOR,
	author_email='python-team@route4me.com',
	description=PROJECT,
	long_description=read_all('README.rst'),
	keywords='route4me, python, sdk, api',
	packages=find_packages(
		include=['route4me.sdk', 'route4me.sdk.*'],
		exclude=['*_test*'],
	),
	zip_safe=True,

	platforms='any',
	classifiers=[
		# 'Development Status :: 1 - Planning',
		# 'Development Status :: 2 - Pre-Alpha',
		# 'Development Status :: 3 - Alpha',
		# 'Development Status :: 4 - Beta',
		# 'Development Status :: 5 - Production/Stable',
		'Development Status :: 2 - Pre-Alpha',
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
		'pydash          ==4.1.0',
	],
	# include_package_data=True,

	# extras_require={
	#     'dev': REQUIREMENTS_DEV,
	# },

	# entry_points='''
	#     [console_scripts]
	#     flask=flask.cli:main
	# '''
)
