from os import path
from setuptools import setup, find_packages

# Content of the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# Setup
setup(
     name = 'meteostat',
     version = '0.3.0',
     author = 'Meteostat',
     author_email = 'info@meteostat.net',
     description = 'Access and analyze historical weather and climate data with Python.',
     long_description = long_description,
     long_description_content_type = 'text/markdown',
     url = 'https://dev.meteostat.net/python/',
     packages = find_packages(),
     include_package_data = True,
     install_requires = ['pandas', 'pyarrow'],
     license = 'MIT',
     classifiers = [
         'Programming Language :: Python :: 3',
         'License :: OSI Approved :: MIT License',
         'Operating System :: OS Independent',
     ],
 )
