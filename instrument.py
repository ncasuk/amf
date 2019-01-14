import csv

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
        parser.add_argument('--outfile', dest="output_file", help="NetCDF output filename")
        parser.add_argument('--metadata', dest="metadata", help="Metadata filename", default='metadata')
        parser.add_argument('infiles',nargs='+', help="Data files to process" )
        parser.add_argument('--outdir', help="Specify directory in which output has to be created.", default="netcdf")
    
        return parser

    def __init__(self, metadatafile, outfile = None):
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

    def get_metadata(self, metafile = 'meta-data.csv'):
        with open(metafile, 'rt') as meta:
            raw_metadata = {} #empty dict
            metaread = csv.reader(meta)
            for row in metaread:
                if len(row) == 2:
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

