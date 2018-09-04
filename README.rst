=========================
NCAS AMF Python Utilities
=========================

How To Use
==========

If you need to use this repository as a library, add it to your repository as
a _submodule_:

``git submodule add https://github.com/ncasuk/amfutils.git amfutils``

You can then import it in Python scripts by:

``import amfutils``

or (e.g. a function from ``read_variables.py``):

``from amfutils.read_variables import read_amf_variables``


``read_variables.py``
---------------------

Reads a CSV export from an AMF Data Project / Data Products / Product Definition Spreadsheets/<instrument> Variables tab and returns a dictionary.

