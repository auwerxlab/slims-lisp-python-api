===================================
A high-level CLI for Slims REST API
===================================

.. image:: https://img.shields.io/badge/license-apache2-brightgreen.svg
   :target: https://github.com/auwerxlab/slims-lisp-python-api/blob/master/LICENSE
.. image:: https://img.shields.io/github/v/release/auwerxlab/slims-lisp-python-api
   :target: https://github.com/auwerxlab/slims-lisp-python-api/releases
.. image:: https://img.shields.io/pypi/v/slims-lisp
   :target: https://pypi.python.org/pypi/slims-lisp

Slims-lisp is a small python package that provides a CLI for Slims REST API.

Features:

- Download a file from a slims experiment attachment step.
- Upload a file to a slims experiment attachment step.

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

slims-lisp fetch
----------------

::

    Usage: slims-lisp fetch [OPTIONS]

      Download a file from a slims experiment attachment step.

    Options:
      --url TEXT                  Slims REST URL. ex:
                                  https://<your_slims_address>/rest/rest
                                  [required]
      --proj TEXT                 Project name (if any).
      --exp TEXT                  Experiment name.  [required]
      --step TEXT                 Experiment step name.  [default:
                                  data_collection; required]
      --active [true|false|both]  Search only in active or inactive steps (or in
                                  both).  [default: true]
      --attm TEXT                 Attachment name.  [required]
      --linked [true|false|both]  Search only linked or unlinked attachments (or
                                  both).  [default: true]
      --output TEXT               Output file name. [default: same as --attm]
      -u, --username TEXT         User name (prompted).  [required]
      -p, --pwd TEXT              Password (prompted).  [required]
      --help                      Show this message and exit.

Output:

- Returns the HTTP GET request response.
- Generates two files (by default in the working directory):

::

    <your_working_directory>
    |── <output>               The requested file
    └── <output>_metadata.txt  Associated metadata in a JSON format

Example:

::

    $ slims-lisp fetch --url <your_slims_url> --proj <your_project_name> --exp <your_experiment_name> --step <your_attachment_step_name> --attm <your_attachment_name>


slims-lisp add
--------------

::

    Usage: slims-lisp add [OPTIONS]
    
      Upload a file to a slims experiment attachment step.
    
    Options:
      --url TEXT                  Slims REST URL. ex:
                                  https://<your_slims_address>/rest/rest
                                  [required]
      --proj TEXT                 Project name (if any).
      --exp TEXT                  Experiment name.  [required]
      --step TEXT                 Experiment step name.  [default: results;
                                  required]
      --active [true|false|both]  Search only in active or inactive steps (or in
                                  both).  [default: true]
      --file TEXT                 Path to the file that will be uploaded.
                                  [required]
      --attm TEXT                 A name to give to the attachement that will be
                                  created. [default: same as --file]
      -u, --username TEXT         User name (prompted).  [required]
      -p, --pwd TEXT              Password (prompted).  [required]
      --help                      Show this message and exit.

Output:

- Returns the HTTP POST request response.

Example:

::

    $ slims-lisp add --url <your_slims_url> --proj <your_project_name> --exp <your_experiment_name> --step <your_attachment_step_name> --file <path/to/your/file>

