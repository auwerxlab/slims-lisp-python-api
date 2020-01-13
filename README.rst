===================================
A high-level CLI for Slims REST API
===================================

Slims-lisp is a small python package that provides a CLI for Slims REST API.

Features:

- Download a file from a slims experiment attachment step.

Resources
=========

- Git clone URL: https://github.com/auwerxlab/slims-lisp-python-api.git
- Documentation: https://github.com/auwerxlab/slims-lisp-python-api
- PyPI repository: https://pypi.org/project/slims-lisp

Installation
============

Slims-lisp can be installed with `pipx`:

::

    $ pipx install slims-lisp

Usage
=====

slims-lisp get
--------------

::

    Usage: slims-lisp get [OPTIONS]

      Download a file and its associated metadata from a slims experiment attachment step.

    Options:
      --url TEXT           Slims REST URL. ex:
                           https://<your_slims_address>/rest/rest  [required]
      --proj TEXT          Project name (if any).
      -e, --exp TEXT       Experiment name.  [required]
      -s, --step TEXT      Experiment step name.  [default: data_collection;
                           required]
      -a, --attm TEXT      Attachment name.  [required]
      -o, --output TEXT    Output file name. [default: same as --attm]
      -u, --username TEXT  User name (prompted).  [required]
      -p, --pwd TEXT       Password (prompted).  [required]
      --help               Show this message and exit.

Output:

::

    <your_working_directory>
    |── <output_file>               The requested file
    └── <output_file>_metadata.txt  Associated metadata in a JSON format

Example:

::

    $ slims-lisp get --url <your_url> --proj <your_project> -e <your_experiment> -s <your_attachment_step> -a <your_attachment_name>

