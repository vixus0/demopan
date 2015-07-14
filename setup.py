"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

setup(
    name='demopan',
    version='0.1',
    description='A cross-platform Source demo organiser',
    url='https://github.com/vixus0/demopan',
    download_url = 'https://github.com/vixus0/demopan/tarball/0.1',
    author='vixus0',
    author_email='vixus0@gmail.com',
    license='WTFPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'License :: Freely Distributable',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='recording demo games steam',
    packages=['demopan'],
    install_requires=['watchdog>=0.8.3'],
    entry_points={
        'console_scripts': [
            'demopan = demopan.__main__:main',
        ],
    },
)
