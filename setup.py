#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requires = ["mkdocs==1.2.2"]

setup_requirements = ["pytest-runner", "pip"]

setup(
    author="Ryan Murray",
    author_email="rymurr@gmail.com",
    url="https://github.com/rymurr/mkdocs-protobuf",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.6",
    description="Mkdocs plugin to render protobuf messages",
    entry_points={
        "mkdocs.plugins": [
            "mkdocs_protobuf=mkdocs_protobuf.plugin:ProtobufDisplay",
        ],
    },
    install_requires=requires,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="mkdocs_protobuf,mkdocs,protobuf",
    name="mkdocs_protobuf",
    packages=find_packages(include=["mkdocs_protobuf", "pymkdocs_protobufnessie.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=[],
    version="0.0.4",
    zip_safe=False,
)
