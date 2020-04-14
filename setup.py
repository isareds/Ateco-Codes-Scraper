# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='AtecoCode Scraper',
    version='0.1.0',
    description='Python script for scraping Italian Ateco Codes',
    long_description=readme,
    author='Isacco Rossi',
    author_email='ir.isacco.rossi@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

