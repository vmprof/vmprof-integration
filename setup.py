from setuptools import setup, find_packages, Extension
import os, sys

setup(
    name='vmprof-integration',
    author='vmprof team',
    author_email='fijal@baroquesoftware.com',
    version="0.0.1.dev0",
    packages=find_packages(),
    description="VMProf's integration tests",
    long_description='See https://vmprof.readthedocs.org/',
    url='https://github.com/vmprof/vmprof-integration',
    install_requires=[
        'requests',
    ],
    tests_require=['pytest'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=False,
    include_package_data=True,
)
