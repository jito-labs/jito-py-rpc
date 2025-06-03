from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='jito_py_rpc',
    version='0.1.5',  # Bump version
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jito Labs',
    author_email='marshall@jito.wtf',
    url='https://github.com/jito-labs/jito-py-rpc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.8',
)
