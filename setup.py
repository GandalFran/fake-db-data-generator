#!/usr/bin/python3
# Copyright 2023 Francisco Pinto Santos
# See LICENSE for details.
# Author: Francisco Pinto Santos (@GandalFran on GitHub)


import io
from setuptools import setup, find_packages


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


def requirements(filename):
    reqs = list()
    with io.open(filename, encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name='fake_db_datagen',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/GandalFran/fake-db-data-generator',
    download_url='https://github.com/GandalFran/fake-db-data-generator/archive/master.zip',
    license='Copyright',
    author='Francisco Pinto-Santos',
    author_email='franpintosantos@usal.es',
    description='Utility to generate fake db data using DBML data models.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(filename='requirements.txt'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts': [
            'fakedatagen=fake_db_datagen.cli:main'
        ],
    },
    python_requires='>=3',
    extras_require={
        "tests": requirements(filename='tests/requirements.txt'),
    },
    keywords=', '.join([
        'DBML', 'Data generation'
    ]),
    project_urls={
        'Bug Reports': 'https://github.com/GandalFran/fake-db-data-generator/issues',
        'Source': 'https://github.com/GandalFran/fake-db-data-generator',
        'Documentation': 'https://github.com/GandalFran/fake-db-data-generator'
    }
)