=========================
NCAS AMF Python Utilities
=========================

How To Use
==========

If you need to use this repository as a library, add it to your repository as
a *submodule*:

``git submodule add https://github.com/ncasuk/amfutils.git amfutils``

You can then import it in Python scripts by:

``import amfutils``

or (e.g. a class from ``instrument.py``):

``from amfutils.instrument import AMFInstrument``


``instrument.py``
---------------------

Generic AMF Instrument class, should be extended for use. You will need at 
least a function to load the raw data into a Pandas Dataframe attribute ``self.rawdata``
(e.g. ``get_data``) and another to convert it to netCDF (e.g. ``netcdf``)
