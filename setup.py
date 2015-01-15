
# NiftyCore - Tomographic Inference 
# Stefano Pedemonte
# Harvard University
# Dec 2013, Boston 


from setuptools import setup, Extension
from glob import glob 



setup(
    name='NiftyCore',
    version='0.1.0',
    author='Stefano Pedemonte',
    author_email='stefano.pedemonte@gmail.com',
    packages=['NiftyCore', 
              'NiftyCore.test', 
              'NiftyCore.NiftyRec', 
              'NiftyCore.NiftyReg', 
              'NiftyCore.NiftySeg', 
              ],
    scripts=[],
    url='http://niftyrec.scienceontheweb.net/',
    license='LICENSE.txt',
    description='Volumetric registration, segmentation and tomographic reconstruction. ',
    long_description=open('README.txt').read(),
    keywords = ["Imaging", "Registration", "Segmentation", "Medical Imaging", "PET", "SPECT", "emission tomography", "transmission tomography", "tomographic reconstruction"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
        "simplewrap >= 0.1.0", 
        "DisplayNode >= 0.1.0", 
    ], 
) 


