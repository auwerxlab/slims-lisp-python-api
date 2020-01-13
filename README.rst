===================================
A high-level CLI for Slims REST API
===================================

Features:
- Download a file from a slims experiment attachment step.

Resources
=========

- Git clone URL: https://github.com/auwerxlab/slims-lisp-python-api.git
- Documentation: https://github.com/auwerxlab/slims-lisp-python-api

Installation
============

::

    $ pipx install slims-lisp

Usage
=====

slims-lisp get
--------------

::

    Usage: slims-lisp get [OPTIONS]

      Download a file from a slims experiment attachment step.

    Options:
      --url TEXT           Slims REST URL.  [default: https://slims-
                           lisp.epfl.ch/rest/rest; required]
      --proj TEXT          Project name (if any).
      -e, --exp TEXT       Experiment name.  [required]
      -s, --step TEXT      Experiment step name. Default: data_collection
                           [default: data_collection; required]
      -a, --attm TEXT      Attachment name.  [required]
      -o, --output TEXT    Output file name. [default: same as --attm]
      -u, --username TEXT  User name (prompted).  [required]
      -p, --pwd TEXT       Password (prompted).  [required]
      --help               Show this message and exit.

Example:

::

    $ slims-lisp get --url <your_url> --proj <your_project> -e <your_experiment> -s <your_attachment_step> -a <your_attachment_name>

