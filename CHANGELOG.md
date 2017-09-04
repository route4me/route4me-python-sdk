# CHANGELOG

The history of changes of the `route4me/route4me-python-sdk` project.

This file **MUST** be filled only by maintainers, using messages from pull
requests.

Please, follow this [guide](http://keepachangelog.com/en/0.3.0/).

## ?? // unreleased

**UPGRAGE TO ALPHA VERSION**

* Optimizations Problem endpoints:
  * list
  * update
  * reoptimize
* `Address` wrapper
* Increase default timeout up to 10 seconds
* First working example (create optimization)

#### Internal features

* Handle datetimes with TZ
* Parse enums function
* `PagedList` - structure for array-like responces
* `TiedList` - wrapper for array-like properties of the main Model

## 2017-08-25 // 0.1.0-dev.8

* Optimizations Problem endpoints:
  * create
  * get (get one)
  * remove

## 2017-08-24 // 0.1.0-dev.7

* network agent
* core error handling (network access, SSL issues)
* scaffold for `Optimizations`

#### Package design

* embed meta variables `__version__`, `__author__` e.t.c
* auto-generated docs
* build for python versions 2.6-3.6 on Travis CI and Appveyor

## 2017-08-13 // 0.1.0-dev.4

**The first version** was published on PyPI.

## 2014-07-01 // 0.0.1

First commit of the package.
