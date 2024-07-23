from setuptools import setup, find_packages

setup(
    name='jito_jsonrpc_sdk',
    packages=find_packages(where='sdk'),
    package_dir={'': 'sdk'},
    install_requires=[
        "requests",
    ],
)