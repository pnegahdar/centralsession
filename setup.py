#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of django-flask-sessions.
# https://github.com/pnegahdar/django-flask-sessions

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2015, Parham Negahdar <pnegahdar@gmail.com>

from setuptools import setup, find_packages
from  centralsession import __version__

setup(
    name='centralsession',
    version=__version__,
    description='A redis based session storage that works for flask and django',
    long_description='''
A redis based session storage that works for flask and django
''',
    keywords='flask django sessions session central ',
    author='Parham Negahdar',
    author_email='pnegahdar@gmail.com',
    url='https://github.com/pnegahdar/centralsessions',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            # 'django-flask-sessions=django_flask_sessions.cli:main',
        ],
    },
)
