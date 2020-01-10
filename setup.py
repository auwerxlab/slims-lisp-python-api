from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'slims-lisp-python-api',
    version = '0.0.1',
    description = 'A high-level CLI for Slims REST API',
    long_description = long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    author = 'Laboratory of Integrative System Physiology (LISP) at EPFL',
    author_email = 'alexis.rapin@epfl.ch',
    url = 'https://github.com/auwerxlab/slims-lisp-python-api',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'slims-lisp = slims_lisp.__main__:cli'
        ]
    },
)
