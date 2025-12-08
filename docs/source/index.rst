.. luvcam documentation master file, created by
   sphinx-quickstart on Fri Nov 28 11:46:11 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


********
LUVCam
********

Welcome to the LUVCam documentation! LUVCam is a package for planning science passes on LUVCam1 and 2. It relies on `NumPy <http://www.numpy.org/>`_ and `Ephem
<https://rhodesmill.org/pyephem/>`_.
- The ability to read from and write to an ordered sequence of files as if it was a single file.

Installation
========
To install the LUVCam package, enter into the command line:
::
   >>> pip install git+https://github.com/emily21030/luvcam.git

.. _usage_toc:
Overview
========
.. toctree::
   :maxdepth: 2

   usage


Reference
========
.. automodapi:: luvcam.visibility_checker
   :no-inheritance-diagram:

