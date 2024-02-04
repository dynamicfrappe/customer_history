from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in customer_history/__init__.py
from customer_history import __version__ as version

setup(
	name="customer_history",
	version=version,
	description="customer_history",
	author="customer_history",
	author_email="hagermossad80@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
