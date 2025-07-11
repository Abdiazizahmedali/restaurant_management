from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in restaurant_management/__init__.py
from restaurant_management import __version__ as version

setup(
	name="restaurant_management",
	version=version,
	description="Complete Restaurant Management System for ERPNext",
	author="Your Company",
	author_email="info@yourcompany.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)