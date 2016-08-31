from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
    windows = [{'script': 'pyburner.py'}],
    data_files=[("", ["config.ini"])],
    zipfile = None,
    )
