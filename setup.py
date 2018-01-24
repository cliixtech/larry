#!/usr/bin/env python

from distutils.core import setup

REQUIREMENTS_FILE = 'requirements.txt'
requirements = []

with open(REQUIREMENTS_FILE) as req_file:
    requirements = req_file.readlines()

setup(
    name='Larry',
    version='1.0',
    description='Simple abstraction to create qrcodes',
    author='Jean Carlos Sales Pantoja',
    author_email='jean@cliix.io',
    url='https://github.com/cliixtech/larry',
    packages=['larry'],
    install_requires=requirements,
    data_files=[
        (
            #'assets/fonts/CaviarDreams',
            '',
            [
                'assets/fonts/CaviarDreams/CaviarDreams_BoldItalic.ttf',
                'assets/fonts/CaviarDreams/Caviar Dreams Bold.ttf',
                'assets/fonts/CaviarDreams/CaviarDreams_Italic.ttf',
                'assets/fonts/CaviarDreams/CaviarDreams.ttf'
            ]
        )
    ]
)
