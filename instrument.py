import csv
import os
import numpy as np
import pandas as pd
from datetime import datetime
from netCDF4 import Dataset


class AMFInstrument:
    """
    Parent class for AMF instruments with common functions
    """
    amf_variables_file = None
    amfvars = {}
    timeformat = '%Y%m%d%H%M%S'

    @staticmethod
    def arguments():
        """
        Processes command-line arguments, returns parser.
        """
        from argparse import ArgumentParser
        parser=ArgumentParser()
        parser.add_argument('--metadata', dest="metadata", help="Metadata filename", default='metadata')
        parser.add_argument('infiles',nargs='+', help="Data files to process" )
        parser.add_argument('--outdir', help="Specify directory in which output has to be created.", default="netcdf")
    
        return parser

    def __init__(self, metadatafile, output_dir = './netcdf'):
        self.base_time = datetime(1970,1,1,0,0,0)
        self.output_dir = output_dir

        #get common attributes
        self.amfvars = self.read_amf_variables(self.amf_variables_file)
        self.raw_metadata = self.get_metadata(metadatafile)
        if 'instrument_name' in self.raw_metadata:
            self.instrument_name = self.raw_metadata['instrument_name'][0]
            self.raw_metadata.pop('instrument_name')
    

    def read_amf_variables(self, csv_var_file):
        """
        Reads an AMF data project CSV-format variable list into a structure.
        """
        out = {}
        with open(csv_var_file,'r') as f:
            varfile = csv.DictReader(f)
            for line in varfile:
                if len(line['Variable']) >0:
                    out[line['Variable']] = {}
                    current_var = line['Variable']
                else:
                    out[current_var][line['Attribute']] = line['Value']

        return out

    def amf_var_to_netcdf_var(self, varname):
        tempvar = self.dataset.createVariable(self.amfvars[varname]['name'], self.amfvars[varname]['type'], dimensions=([x.strip() for x in self.amfvars[varname]['dimension'].split(',')]), fill_value = self.amfvars[varname]['_FillValue'])
        tempvar.long_name = self.amfvars[varname]['long_name']
        tempvar.units = self.amfvars[varname]['units']
        tempvar.coordinates = self.amfvars[varname]['coordinates']
        tempvar.cell_methods = self.amfvars[varname]['cell_methods']
        tempvar.dimension = self.amfvars[varname]['dimension']
        tempvar.type = self.amfvars[varname]['type']
        if(self.amfvars[varname]['standard_name']):
            tempvar.standard_name = self.amfvars[varname]['standard_name']

        return tempvar



    def get_metadata(self, metafile = 'meta-data.csv'):
        with open(metafile, 'rt') as meta:
            raw_metadata = {} #empty dict
            metaread = csv.reader(meta)
            for row in metaread:
                if len(row) == 2 and row[0] != 'Variable':
                    raw_metadata[row[0]] = row[1:]
            return raw_metadata


    def filename(self, variable, version):
        """
        creates a correctly-formed AMF filename for the output netcdf file
        """
        file_elements = [
                self.instrument_name,
                self.raw_metadata['platform_name'][0],
                self.time_coverage_start,
                variable,
                'v' + version 
                ]
        self.outfile = "_".join(file_elements) + '.nc'
        return self.outfile

    def setup_dataset(self, product, version):
        """
        instantiates NetCDF output
        """
        self.dataset = Dataset(os.path.join(self.output_dir, self.filename("nox-noxy-concentration","1")), "w", format="NETCDF4_CLASSIC")

        # Create the time dimension - with unlimited length
        time_dim = self.dataset.createDimension("time", None)
    
        # Create the time variable
        self.rawdata['timeoffsets'] = (self.rawdata.index - self.base_time).total_seconds()
    
        time_units = "seconds since " + self.base_time.strftime('%Y-%m-%d %H:%M:%S')
        time_var = self.dataset.createVariable("time", np.float64, dimensions=("time",))
        time_var.units = time_units
        time_var.axis = 'T'
        time_var.standard_name = "time"
        time_var.long_name = "Time (%s)" % time_units
        time_var.calendar = "standard"
        time_var.type = "float64"
        time_var.dimension = "time"
        time_var[:] = self.rawdata.timeoffsets.values


    def land_coordinates(self):

        #create the location dimensions - length 1 for stationary devices
        lat  = self.dataset.createDimension('latitude', 1)
        lon  = self.dataset.createDimension('longitude', 1)
    
        #create the location variables
        latitudes = self.dataset.createVariable('latitude', np .float32,  ('latitude',))
        latitudes.units = 'degrees_north'
        latitudes.standard_name = 'latitude'
        latitudes.long_name = 'Latitude'
    
        longitudes = self.dataset.createVariable('longitude', np .float32,  ('longitude',))
        longitudes.units = 'degrees_east'
        longitudes.standard_name = 'longitude'
        longitudes.long_name = 'Longitude'
    
        longitudes[:] = [self.raw_metadata['platform_longitude']]
        latitudes[:] = [self.raw_metadata['platform_latitude']]
    
        #remove lat/long
        self.raw_metadata.pop('platform_longitude',None)
        self.raw_metadata.pop('platform_latitude',None)

