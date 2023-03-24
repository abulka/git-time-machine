import os
from setuptools import setup, find_packages
import sys
print(sys.path)
print("on linux please run: sudo apt-get install dpkg-dev build-essential python3-dev freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libgstreamer-plugins-base1.0-dev libgtk-3-dev libjpeg-dev libnotify-dev libpng-dev libsdl2-dev libsm-dev libtiff-dev libwebkit2gtk-4.0-dev libxtst-dev")
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name='git time machine',
    version='1.0.0',
    url='https://github.com/abuka/git-time-machine',
    author='Andy Bulka',
    author_email='abulka@gmail.com',

    py_modules=['main'],

    # install_requires=[
    #     # Add your requirements here
    # ],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'git-tm=main:run',
        ],
    },    
)
