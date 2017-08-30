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
    create .bat file
    to submit rerender of failed server\'s frames
    with Autodesk Backburner
    ''',
    setup_requires=['py2app']
)

