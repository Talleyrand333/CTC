from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in ctc/__init__.py
from ctc import __version__ as version

setup(
	name='ctc',
	version=version,
	description='Corona Test Center Application',
	author='Talleyrand',
	author_email='ebukaakeru@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
