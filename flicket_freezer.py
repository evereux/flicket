#! /usr/bin/python3.6

"""
    A script to create a zip of the flicket application for release.
"""

import os
from zipfile import ZipFile, ZIP_DEFLATED

from application import __version__

exclude_dirs = [
    '.git',
    '.idea',
    'dist',
    'env',
    'tmp',
    '__pycache__',
    '__archive__',
    'docs']

exclude_files = [
    '.gitignore',
    'alembic.ini',
    'config.json',
    'flicket_freezer.py'
]


def zip_files(path, zipper):
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            rel_path = os.path.relpath(root, path)
            zipper.write(os.path.join(rel_path, file))


bundle_name = 'flicket_{}.zip'.format(__version__)

current_path = os.getcwd()
bundle_name = os.path.join(current_path, 'dist', bundle_name)

with ZipFile(bundle_name, 'w', ZIP_DEFLATED) as zipper:
    zip_files(os.getcwd(), zipper)
