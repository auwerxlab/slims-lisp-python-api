# A high-level CLI for Slims REST API

Features:
- Download a file from a slims experiment attachment step.

# Resources

- Git clone URL: https://github.com/auwerxlab/slims-lisp-python-api.git
- Documentation: https://github.com/auwerxlab/slims-lisp-python-api

# Getting this project

Use git to clone this project where you need it.
```
$ git clone https://github.com/auwerxlab/slims-lisp-python-api.git
```

# Usage

#### slims_import.py
<pre>
Usage: slims_import.py [OPTIONS]

  Download a file from a slims experiment attachment step.

Options:
  --slims_url TEXT     Slims REST URL.  [required]
  --proj TEXT          Project name.
  --exp TEXT           Experiment name.  [required]
  --step TEXT          Experiment step name.  [required]
  -a, --attm TEXT      Attachment name.  [required]
  -o, --output TEXT    Output file name.
  -u, --username TEXT  User name.  [required]
  -p, --pwd TEXT       Password.  [required]
  --help               Show this message and exit.
</pre>

