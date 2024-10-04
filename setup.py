from setuptools import setup, find_packages

setup(
    name='jito_py_rpc',
    version='0.1.0',
    packages=find_packages(where='sdk'),
    package_dir={'': 'sdk'},
    install_requires=[
        "requests",
    ],
)