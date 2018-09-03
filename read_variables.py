import csv

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
