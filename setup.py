from setuptools import setup

setup(
   name='inTriplicate',
   version='0.0.1',
   description='A module for making SD card backups better',
   author='Matthew Bennett',
   author_email='twinbee@gmail.com',
   packages=['inTriplicate'],  #same as name
   install_requires=['burn'], #external packages as dependencies
)