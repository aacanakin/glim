from setuptools import setup
import os
from os.path import exists

v = "0.10.7"

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    author='Aras Can Akin',
    author_email='aacanakin@gmail.com',
    name='glim',
    packages=find_packages(),
    version=v,
    description='A modern framework for the web',
    long_description=read('README.rst'),
    entry_points={
        'console_scripts': ['glim=glim.cli:main']
    },
    url='https://github.com/aacanakin/glim',
    download_url='https://github.com/aacanakin/glim/archive/v%s.zip' % v,
    keywords=[
        'framework',
        'web framework',
        'api development',
        'model view controller',
        'Werkzeug',
        'SQLAlchemy',
        'Jinja2',
        'termcolor',
    ],
    install_requires=[
        "Werkzeug >= 0.10.1",
        "termcolor"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
