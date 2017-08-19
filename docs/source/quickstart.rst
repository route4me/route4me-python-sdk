Quick Start
===========

Quick start guide

Install
-------

The best way --- use PIP:

.. code-block:: bash

    $ pip install route4me-sdk

Run
---

.. code-block:: python

    import route4m.sdk

    r4m = route4me.sdk.Route4Me(api_key='1111111')
    print(r4m.version)
