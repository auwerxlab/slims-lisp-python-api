===================================
A high-level CLI for Slims REST API
===================================

.. image:: https://img.shields.io/badge/license-apache2-brightgreen.svg
   :target: https://github.com/auwerxlab/slims-lisp-python-api/blob/master/LICENSE

.. image:: https://img.shields.io/github/v/release/auwerxlab/slims-lisp-python-api.svg
   :target: https://github.com/auwerxlab/slims-lisp-python-api/releases

.. image:: https://img.shields.io/pypi/v/slims-lisp.svg
   :target: https://pypi.python.org/pypi/slims-lisp

.. image:: https://readthedocs.org/projects/slims-lisp-python-api/badge/?version=latest
   :target: https://slims-lisp-python-api.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Slims-lisp is a small python package that provides a CLI for SLIMS REST API.

Features:

- Download a file from a SLIMS experiment attachment step.
- Upload a file to a SLIMS experiment attachment step.
- Create a new SLIMS experiment attachment step and upload multiple files to it
  (useful to upload a whole dataset containing multiple data and/or metadata files at once).

Installation
============

The latest release is available on PyPI and can be installed using ``pip``:

::

    $ pip install slims-lisp

Isolated environments using ``pipx``
------------------------------------

Install and execute slims-lisp in an isolated environment using ``pipx``.

`Install pipx <https://github.com/pipxproject/pipx#install-pipx>`_
and make sure that the ``$PATH`` is correctly configured.

::

    $ python3 -m pip install --user pipx
    $ pipx ensurepath

Once ``pipx`` is installed use following command to install ``slims-lisp``.

::

    $ pipx install slims-lisp
    $ which slims-lisp
    ~/.local/bin/slims-lisp

Usage
=====

The latest documentation is available on `https://readthedocs.org <https://slims-lisp-python-api.readthedocs.io/en/latest/>`_.
