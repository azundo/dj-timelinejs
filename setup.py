# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='dj-timelinejs',
    version='0.1.0',
    author='Ben Best',
    author_email='ben.best@gmail.com,',
    packages=['timelinejs'],
    include_package_data=True,
    url='https://github.com/azundo/dj-timelinejs/',
    license='BSD license and MPL 2.0, see LICENSE',
    description='Support for serving TimelineJS from Django sites.',
    long_descript=open('README.md').read(),
)
