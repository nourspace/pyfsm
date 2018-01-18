#!/usr/bin/env python
"""Setup to install Python Finite State Machine."""
from distutils.core import setup

setup(name='btcde',
      version='1.0',
      py_modules=['pyfsm'],
      install_requires=[],
      description='Simple Finite State Machine implementation in Python 3.',
      url='https://github.com/nourchawich/pyfsm',
      author='Nour Chawich',
      author_email='mo.chawich@gmail.com',
      license='MIT',
      classifiers=[
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries :: Application '
                   'Frameworks',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6', ],
      keywords='finite state machine fsm',
      )
