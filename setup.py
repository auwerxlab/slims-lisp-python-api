from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="slims-lisp-python-api",
    version="0.0.1",
    author="Laboratory of Integrative System Physiology (LISP) at EPFL",
    author_email="alexis.rapin@epfl.ch",
    description="A high-level CLI for Slims REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/auwerxlab/slims-lisp-python-api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
