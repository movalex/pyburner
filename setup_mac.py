from setuptools import setup

APP = ['pyburner.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': False}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    DATA_FILES=["config.ini"],
    version = '0.0.1',
    name = 'pyBurner', 
    description = '''
    create .bat file
    to submit rerender of failed server\'s frames
    with Autodesk Backburner
    ''',
    setup_requires=['py2app']
)

