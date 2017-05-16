#!/usr/bin/env python
# coding: utf-8
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Setup script for Photon."""
import os
import setuptools


readme = ''
if os.path.exists('README.md'):
    with open('README.md') as readme_file:
        readme = readme_file.read()

changes = ''
if os.path.exists('CHANGES.md'):
    with open('CHANGES.md') as changes_file:
        changes = changes_file.read()

test_requirements = []

setuptools.setup(
    name = 'photon',
    version = '0.1.0',
    description = "A utility for managing RAM disks.",
    long_description = '%s\n\n%s' % (readme, changes),
    author = "Christoph Diehl",
    author_email = 'cdiehl@mozilla.com',
    url = 'https://github.com/MozillaSecurity/photon',
    packages = setuptools.find_packages(),
    package_dir = {'photon': 'photon'},
    include_package_data = True,
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'photon = photon.photon:main',
        ]
    },
    license = "MPL 2.0",
    keywords = 'photon',
    classifiers = [
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
