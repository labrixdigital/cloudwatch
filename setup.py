from setuptools import setup, find_packages, Extension
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='cloudwatch',
    version='1.0.5',
    description='A small handler for AWS Cloudwatch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/labrixdigital/cloudwatch',
    author='Ernesto Monroy',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    install_requires = ['boto3'],
    keywords='cloudwatch aws boto3 logging logger',
    packages=find_packages(include=['cloudwatch']),
    python_requires='>=3.5',
    project_urls={
        'Bug Reports': 'https://github.com/labrixdigital/cloudwatch/issues',
        'Source': 'https://github.com/labrixdigital/cloudwatch',
    },
)