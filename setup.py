
# NiftyPy  
# Stefano Pedemonte
# Harvard University
# Dec 2013, Boston 


# Use old Python build system, otherwise the extension libraries cannot be found. FIXME 
import sys
for arg in sys.argv: 
    if arg=="install":
        sys.argv.append('--old-and-unmanageable') 

from setuptools import setup, Extension
try: 
    from setuptools.extension import Library
except: 
    from setuptools import Library 
from glob import glob 



setup(
    name='NiftyPy',
    version='0.2.0',
    author='Stefano Pedemonte',
    author_email='spedemonte@mgh.harvard.edu',
    packages=['NiftyPy', 
              'NiftyPy.test', 
              'NiftyPy.NiftyRec', 
              'NiftyPy.NiftyReg', 
              'NiftyPy.NiftySeg', 
              ],
    scripts=[],
    url='http://www.occiput.io/',
    license='LICENSE.txt',
    description='Python wrapper for NiftyRec, NiftyReg and NiftySeg: tomographic reconstruction, volumetric registration and segmentation.',
    long_description=open('README.rst').read(),
    keywords = ["Imaging", "Registration", "Segmentation", "Medical Imaging", "PET", "SPECT", "emission tomography", "transmission tomography", "tomographic reconstruction"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
                     ],
    install_requires=[
        "numpy >= 1.6.0", 
        "simplewrap >= 0.2.0", 
        "DisplayNode >= 0.2.0", 
    ], 
) 


