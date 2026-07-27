# -*- coding: utf-8 -*-
"""Compatibility shim.

All packaging metadata lives in ``pyproject.toml`` (PEP 621) and the canonical
build backend is hatchling. This file exists only so tooling that still shells
out to ``python setup.py <command>`` keeps working; setuptools >= 77 reads the
``[project]`` table directly, so no metadata is duplicated here.

Prefer the standard commands:

    python -m build          # instead of: python setup.py sdist bdist_wheel
    pip install -e .         # instead of: python setup.py develop
    pip install .            # instead of: python setup.py install
"""

from setuptools import setup

setup()
