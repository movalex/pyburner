from setuptools import setup
# import sys

APP = ['pyburner.py']
DATA_FILES = ["config.ini"]
OPTIONS = {'argv_emulation': True}
# sys.argv.append('py2app -A')

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    version = '0.0.1',
    name = 'pyBurner', 
    description = '''
    create .bat file to resubmit 3DMax network render job with chosen frames
    ''',
    setup_requires=['py2app']
)
