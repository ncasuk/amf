import csv

class AMFInstrument:
    """
    Parent class for AMF instruments with common functions
    """

    def read_amf_variables(csv_var_file):
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

    def arguments():
        """
        Processes command-line arguments, returns parser.
        """
        from argparse import ArgumentParser
        parser=ArgumentParser()
        parser.add_argument('--outfile', dest="output_file", help="NetCDF output filename", default='sonic_2d_data.nc')
        parser.add_argument('--metadata', dest="metadata", help="Metadata filename", default='2d-sonic-metadata')
        parser.add_argument('infiles',nargs='+', help="Gill 2D Windsonic data files" )
        parser.add_argument('--outdir', help="Specify directory in which output has to be created.", default="netcdf")
    
        return parser
