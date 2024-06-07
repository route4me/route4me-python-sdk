# CHANGELOG

This is the history of changes of the `route4me-python` package

> This file should be filled by maintainers, using pull requests
> Please, follow this [guide](https://keepachangelog.com/en/1.0.0/)

## [0.0.7.0] - 2020-09-01

### Removed

-   Python 2 support
-   Pypy build
-   Set Tracking Data Test

### Added

-   Documentation
-   Changelog file
-   Tox
-   MANIFEST file
-   VERSION file

### Fixed

-   Bug in Optimization Callback example
-   Some Test Cases that were failing

### Changed

-   setup.py
-   Travis config file

## [0.0.6.1] - 2019-11-11

### Added

-   Added Exception when the server could not geo-code some addresses

## [0.0.6.1] - 2019-11-06

### Added

-   Redirect flag to QS when redirects are disable

### Fixed

-   Bug on batch geocoding

## [0.0.6.0] - 2019-10-24

### Changed

-   Batch Geocodig method converted to POST request.

### Fixed

-   Bug that assign the geo-coordinates to the wrong addresses

## [0.0.5.2] - 2018-08-24

### Changed

-   All Examples to work with JSON response

### Fixed

-   Some Bugs

## [0.0.5.1] - 2018-08-22

### Changed

-   Changed all responses to JSON.

### Fixed

-   All examples to support JSON response
-   GPS Test

## [0.0.5.0] - 2018-02-26

### Added

-   Address-Book example to query for any field

### Removed

-   Lib xmltodict dependency.
-   Limit and offset as required fields in addressbook service

### Changed

-   Addresses service

## [0.0.4.0] - 2017-08-03

### Added

-   Optimized Callback URL feature and example

## [0.0.3.11] - 2016-11-02

### Added

-   Python 3 support

## [0.0.3.10] - 2016-09-19

### Added

-   Routes Management and Missing Examples

## [0.0.3.9] - 2016-09-16

### Added

-   Members Management

## [0.0.3.8] - 2016-09-12

### Added

-   Activity Feed Support and Examples
-   Optimization missing Examples
-   Rapid Address missing Examples, remove python env from all examples, moved geocoding examples to its own folder
-   File Uploading feature and examples
-   Avoidance Zone missing Examples

## [0.0.3.7] - 2016-07-25

### Added

-   Territory Support

## [0.0.3.6] - 2016-07-14

### Added

-   Rapid Address Support and Examples
-   Optimization Example

## [0.0.3.5] - 2016-06-22

### Added

-   Orders support

## [0.0.3.4] - 2016-04-22

### Added

-   Avoidance Zone Management
-   Address Book Management, Route Tracking

## [0.0.3.3] - 2016-04-18

### Added

-   Generic Example, Notes, Delete Route, Single Depot Multiple Driver, Single Depot Multiple Driver TW Examples and Features

## [0.0.3.2] - 2016-03-24

### Added

-   Activities, Optimizations, Routes, Telematics, and Users Examples
-   Notes, and Activities Services

## [0.0.3.1] - 2016-01-21

### Added

-   Trucking hazardous goods features

## [0.0.3.0] - 2016-01-19

### Added

-   Example to update address attributes/details in an existing route (i.e. custom data, alias, order details, weight)
-   Example to insert address into existing route
-   Example to remove address from existing route
-   Example to move address from one stop into another

## [0.0.2.14] - 2015-12-17

### Added

-   Optimization trucking parameters and min_tour_size

## [0.0.2.13] - 2015-12-03

### Changed

-   Exceptions and Algorithm Type verification

## [0.0.2.12] - 2015-11-28

### Added

-   Optimization parameters, added support to Algorithm 100 and 101

## [0.0.2.11] - 2015-08-13

### Fixed

-   Examples

## [0.0.2.10] - 2015-07-16

### Added

-   Turns Avoidance uturn and leftturn support

## [0.0.2.9] - 2015-05-12

### Changed

-   Enabled follow redirects feature

## [0.0.2.8] - 2015-04-27

### Added

-   Optimization parameter max_tour_size

## [0.0.2.7] - 2015-04-22

### Added

-   Disable redirects

## [0.0.2.6] - 2015-04-19

### Added

-   Retry feature in case of geocoding error

## [0.0.2.5] - 2015-04-08

### Changed

-   Multiple depot multiple driver example

### Added

-   Geo-localization getter retry functionality in case of failure

## [0.0.2.4] - 2015-04-01

### Added

-   Optimization quality and route start date feature
-   Geocoding Example

## [0.0.2.3] - 2015-03-31

### Fixed

-   Multiple Depot, Multiple Driver, Time window Example

## [0.0.2.2] - 2015-03-01

### Added

-   API Endpoints
-   Batch and single address geocoding

## [0.0.2.1] - 2015-02-20

### Added

-   Route Exporter feature

## [0.0.2.0] - 2015-02-19

### Added

-   Geocoding feature

## [0.0.1.0] - 2014-07-01

### Added

-   First commit of the package.
