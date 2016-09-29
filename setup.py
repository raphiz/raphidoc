#!/usr/bin/env python
# encoding: utf-8

import os
from setuptools import setup, find_packages


setup(
    name="raphidoc",
    version="0.1.0.dev0",
    packages=['raphidoc'],
    author="Raphael Zimmermann",
    author_email="dev@raphael.li",
    url="https://github.com/raphiz/raphidoc",
    description="The way I want to write my notes...",
    long_description=("For more information, please checkout the `Github Page "
                      "<https://github.com/raphiz/raphidoc>`_."),
    license="GPLv3",
    platforms=["Linux", "BSD"],
    include_package_data=True,
    zip_safe=False,
    install_requires=open('./requirements.txt').read(),
    test_suite='tests',
    entry_points={
        'console_scripts':
            ['raphidoc = raphidoc.cli:main']
    },

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        "Programming Language :: Python :: Implementation :: CPython",
        'Development Status :: 4 - Beta',
    ],
)
