from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
    windows = [{'script': 'pyburner.py'}],
    data_files=[("", ["config.ini"])],
    version = '0.0.1',
    name = 'pyBurner', 
    description = '''
    create .bat file to resubmit 3DMax network render job with certain frames
    ''',
    zipfile = None,
    )
