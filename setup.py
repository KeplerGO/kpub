#!/usr/bin/env python
from setuptools import setup


# PyPi requires reStructuredText instead of Markdown,
# so we convert our Markdown README for the long description
try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   long_description = open('README.md').read()

# Command-line tools
entry_points = {'console_scripts': [
    'kpub = kpub:kpub',
    'kpub-add = kpub:kpub_add',
    'kpub-update = kpub:kpub_update',
    'kpub-import = kpub:kpub_import',
    'kpub-export = kpub:kpub_export',
]}

setup(name='kpub',
      version='1.0.0',
      description="A simple tool to keep track of the publications related "
                  "to NASA's Kepler/K2 mission.",
      long_description=long_description,
      author='Geert Barentsen',
      author_email='hello@geert.io',
      license='MIT',
      url='http://barentsen.github.io/kpub',
      packages=['kpub'],
      install_requires=["jinja2"],
      entry_points=entry_points,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering :: Astronomy",
          ],
      )

#      dependency_links=["https://github.com/barentsen/ads/archive/e4b98388ea68887f642e53b4574f179cbd715703.tar.gz"],    
