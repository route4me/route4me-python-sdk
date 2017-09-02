.. include:: common.rst

Quick Start
===========

Quick start guide

Install
-------

Probably, the best and simplest way --- use PIP:

.. code-block:: bash

    $ pip install route4me-sdk

.. seealso::

	The full installation guide: :doc:`/install`

Use
---

.. code-block:: python

    import route4m.sdk

    r4m = route4me.sdk.ApiClient(api_key='11111111111111111111111111111111')
    print(r4m.version)

    opt = r4m.optimizations.get('07372F2CF3814EC6DFFAFE92E22771AA')
    print(opt)
