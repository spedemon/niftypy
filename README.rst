=========
NiftyPy
=========

Registration, segmentation, tomographic reconstruction. 
Python wrapper of NiftyRec, NiftyReg and NiftySeg. 

Typical usage looks like this:

#!/usr/bin/env python
from NiftyPy import NiftyRec


... more documentation is required, for now look at how this package is utilized in occiput.io
While NiftyPy is just a Python wrapper of the NiftyRec, NiftyReg and NiftySeg libraries, occiput.io provides a high level interface for tomographic reconstruction (SPECT, PET, CT) and for other imaging tasks. It’s easies, with occiput.io, to define the system geometry and reconstruct with iterative algorithms. 


Installation
============

Linux, MacOsX, Win
------------------

There are two ways to install under Linux and MacOsX and Windows: 

1. If you have pip installed: 

pip install niftypy

2. download source files, uncompress, at the command line cd to the downloaded folder and run: 

python setup.py build test install 


Website
=======

`NiftyPy home page <http://www.occiput.io/>`_. 



