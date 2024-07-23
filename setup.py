from setuptools import setup, find_packages

setup(
    name='sdk/jito_jsonrpc_sdk.py',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
)