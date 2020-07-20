"""wheel setup for Prosper common utilities"""
from codecs import open
import importlib
from os import path, listdir

from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
__package_name__ = 'ProsperCommon'
__library_name__ = 'common'

def get_version(package_name):
    """find __version__ for making package

    Args:
        package_name (str): path to _version.py folder (abspath > relpath)

    Returns:
        str: __version__ value

    """
    module = 'prosper.' + package_name + '._version'
    package = importlib.import_module(module)

    version = package.__version__

    return version

def hack_find_packages(include_str):
    """patches setuptools.find_packages issue

    setuptools.find_packages(path='') doesn't work as intended

    Returns:
        list: append <include_str>. onto every element of setuptools.find_pacakges() call

    """
    new_list = [include_str]
    for element in find_packages(include_str):
        new_list.append(include_str + '.' + element)

    return new_list

def include_all_subfiles(*args):
    """Slurps up all files in a directory (non recursive) for data_files section

    Note:
        Not recursive, only includes flat files

    Returns:
        list: list of all non-directories in a file

    """
    file_list = []
    for path_included in args:
        local_path = path.join(HERE, path_included)

        for file in listdir(local_path):
            file_abspath = path.join(local_path, file)
            if path.isdir(file_abspath):    #do not include sub folders
                continue
            file_list.append(path_included + '/' + file)

    return file_list

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name=__package_name__,
    description='Common Utilities for EVEProsper Projects',
    version=get_version(__library_name__),
    long_description=readme,
    author='John Purcell',
    author_email='prospermarketshow@gmail.com',
    url='https://github.com/EVEprosper/' + __package_name__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='prosper eve-online webhooks logging configuration-management',
    packages=hack_find_packages('prosper'),
    include_package_data=True,
    package_data={
        '': ['LICENSE', 'README.rst'],
    },
    entry_points={
        'console_scripts': [
            'make_gunicorn_config=prosper.common.flask_utils:make_gunicorn_config',
        ],
    },
    install_requires=[
        'anyconfig',
        'anytemplate',
        'jinja2',
        'plumbum',
        'requests',
        'semantic_version',
    ],
    extras_require={
        'dev':[
            'sphinx',
            'sphinxcontrib-napoleon',
        ],
    },
)
