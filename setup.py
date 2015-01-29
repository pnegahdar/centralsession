#!/usr/bin/env python

from distutils.core import setup

setup(name='centralsession',
      version='0.1',
      description='Centralizing Sessions including Flask and Django',
      author='Parham Negahdar',
      author_email='pnegahdar@gmail.com',
      packages=['centralsession'],
)

from setuptools import setup

setup(name='centralsession',
      version='0.1',
      description='Centralizing Sessions including Flask and Django',
      url='https://github.com/pnegahdar/centralsession',
      author='Parham Negahdar',
      author_email='pnegahdar@gmail.com',
      license='MIT',
      install_requires=[
          'Django>=1.4',
          'Flask>=0.10',
          'redis>=2.0',
      ],
      packages=['centralsession']
)
