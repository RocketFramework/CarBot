# setup.py
from setuptools import setup, find_packages

setup(
    name='CARBOT',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'my_command = my_package.module:main',  # command = package.module:function
        ],
    },
)