""" Audit postal codes"""

import csv
import xml.etree.cElementTree as ET


""" I found a data set with the postal codes of the entire Buenos Aires province and now I want to verify if the codes
that I got, match with the ones in the file.
This is where I found the postal codes: https://yadi.sk/d/WIc5FNVEtk9U8 """


def audit_postal_codes():
    """ Process postal codes from osm data from Buenos Aires province, Argentina

    Returns:
        strangepc_dict(dict): containing postal codes from the function deal_strange_pc
        invalid_pc(set): postal codes whose length < 4
        not_in_set_pc(set): postal codes not found in the validation data obtained from a different source
            (set_postalcodes)"""

    invalid_pc, not_in_set_pc, not_in_set_cut, strange_pc = process_pc_sets()
    strangepc_dict = deal_strange_pc(strange_pc)
    return strangepc_dict, invalid_pc, not_in_set_pc


def get_postalcode_set(csv_file):
    """ Creates a set of the all postal codes found in the csv data set (https://yadi.sk/d/WIc5FNVEtk9U8)

    Args:
        csv_file(str): the Buenos Aires postal codes dataset
    Returns:
        postal_codes(set): a set of the postal codes in the csv"""

    postal_codes = set()
    with open(csv_file, "r") as csvfile:
        csvread = csv.reader(csvfile)
        next(csvread, None)  # to start from the second row
        for row in csvread:
            p_code = row[1][1:5]
            postal_codes.add(p_code)
    return postal_codes


"""Now I want to verify the match between the postal codes set and the ones in the osm data"""


def verify_postal_codes(osm):
    """ Audits postal codes from a Buenos Aires osm file

    Args:
        osm: input Buenos Aires OSM data
    Returns:
        invalid_pc(set): This set will contain the postal codes whose length is < 4
        not_in_set_pc(set): Postal codes not found in the set_postalcodes set
        not_in_set_cut(list): A list containing the postal codes whose length is >4 that were cutted and are not in
            the set
        strange_pc(set): Strange postal codes who did not enter in any of the above cases
        """
    set_postalcodes = get_postalcode_set("BA_postalcodes.csv")
    invalid_pc = set()
    in_set_pc = set()  # Postal codes found in the valid postal codes set (set_postalcodes)
    not_in_set_pc = set()
    not_in_set_cut = []
    strange_pc = set()
    tree = ET.parse(osm)
    root = tree.getroot()
    for child in root:
        if child.tag == "node":
            for tag in child.iter("tag"):
                if get_postal_code(tag):
                    p_code = tag.attrib['v']
                    if len(p_code) < 4:
                        invalid_pc.add(p_code)
                    elif len(p_code) == 4 and (p_code in set_postalcodes):
                        in_set_pc.add(p_code)
                    elif len(p_code) == 4 and (p_code not in set_postalcodes):
                        not_in_set_pc.add(p_code)
                    elif len(p_code) == 8:
                        p_code4 = p_code[1:5]
                        if p_code4 not in set_postalcodes:
                            not_in_set_cut.append(p_code4)
                        else:
                            in_set_pc.add(p_code4)
                    else:
                        strange_pc.add(p_code)
    return invalid_pc, not_in_set_pc, not_in_set_cut, strange_pc


def get_postal_code(elem):
    """ Given a tag of a osm file, this returns postal code for a given attribute

    Args:
        elem(Element)
    """
    return elem.attrib['k'] == "addr:postcode"


def process_pc_sets():
    """ Individually process the postal codes sets returned from verify_postal_codes"""

    invalid_pc, not_in_set_pc, not_in_set_cut, strange_pc = verify_postal_codes("buenos-aires_argentina.osm")

    """
    Now I want to study all the postal codes that did not appear in the set_postalcodes to analyze if the codes 
    actually exist and are missing in the csv file or if those are invalid postal codes.
    
    To do this, I'll analyze each of the not_in_set_pc variable and google them to see if I find them:
    
    not_in_set_pc {'1720', '0237', '1299', '1404', '1523', '1475', '0000', '1515', '1776', '1522', '1000', 
    '!923', '1418', '1456', '1423'}
    
    - 1776: corresponds to 'localidad 9 de Abril', in Buenos Aires province and this matches with the data in the osm
    - 1423: does exists, corresponds to a place in 'San Isidro' but in the osm file, this is the only occurrence and does
    not match with the place it's supposed to be
    - !923: does not exist
    - 0237: does not exist
    - 1418: does not exist
    - 1456: does not exist
    - 1299: exists but does not correspond to the place in the osm
    - 1000: does not exist
    - 0000: does not exist
    - 1523: does not exist
    - 1720: does not exist
    - 1522: does not exist
    - 1475: does not exist
    - 1515: does not exist
    - 1404: does not exist
    
    All of the postal codes that do not exist only appear once in the whole document"""

    """ Analyzing all of the postal codes from strange_pc set:
    strange_pc {'B1629', '1619, 1623', 'C1439AG', '1170ACG', 'C1006', 'B1663', 'B1631', 'B1702', 'P1091', '1.619', 
    'C1107', '70000', '1686S', '1425AAJ', 'B1653', 'B1900', '1.852'}
    
    All of the postal codes who entered in this set have a length > 4 but < 8 and most of them start with a letter, 
    which makes me think that they were not entered correctly in openstreetmap, as that notation seems to be a mix 
    between the old one (only 4-digit numbers) and the new one (8-character postal codes)
    
    I'll analyze each of the codes individually:
     
    - 1425AAJ -> 1425 -> corresponds to Recoleta, a neighborhood in Buenos Aires 
    - 70000 does not exist
    - C1107 -> 1107 -> Juana Manso from 602 to 700, a street in Buenos Aires
    - B1702 -> 1702 -> Ciudadela and Jose Ingenieros
    - B1663 -> 1663 -> Muñiz or San Miguel
    - C1006-> 1006 -> Calle Maipu from 701 to 799 in Buenos Aires.
    - B1631 -> 1631 -> Localidad Villa Rosa
    - C1439AG -> 1439 -> Calle Soldado De La Frontera from 5001 to 5099 in Buenos Aires.
    - 1170ACG -> 1170 -> Calle Dr Tomas De Anchorena, from 501 to 599 
    - B1653 -> 1653 -> Villa Ballester
    - P1091 -> 1091 -> Moreno
    - B1900 -> 1900 -> La Plata
    - 1.852 -> 1852 -> Ministro Rivadavia or Burzaco
    - B1629 -> 1629 -> Almirante Irizar, Barrio San Alejo
    - 1686S -> 1686 -> Hurlingham and William Morris	
    - '1619, 1623': The actual postal code for that point in the osm is 1625"""

    """From not_in_set_cut:    
    not_in_set_cut ['anfi', '1652']
    Neither of the two exist"""

    """ As almost all of the postal codes in strange_pc do exist and the value 70000 is the only one that does not exist,
    I'm going to move the 70000 element from the strange_pc set to the not_in_setpc so I can later modify all of the
    remaining postal codes in strange_pc"""
    strange_pc.remove('70000')
    invalid_pc.add('70000')
    return invalid_pc, not_in_set_pc, not_in_set_cut, strange_pc


def deal_strange_pc(strange_set):
    """Given the results of the analysis of the strange_set, this function modifies each of the postal codes to make
    them comply with the four-digit format

    Args:
        strange_set(set)
    Returns:
        strange_dic(dict)
        """
    strange_dic = {}
    for val in strange_set:
        if val[1] == '.':
            new_val = val.replace('.', '')
            strange_dic[val] = new_val
        elif len(val) > 8:
            strange_dic[val] = '1625'
        elif is_int(val[0]):
            strange_dic[val] = val[:4]
        else:
            strange_dic[val] = val[1:5]
    """ Now, I'm going to add the value from the not in set variable that is an actual postal code and is not 
    in the set_postalcodes"""
    strange_dic['1776'] = '1776'
    return strange_dic


def is_int(string):
    """ Evaluates if a string can be changed to int and returns a boolean"""
    try:
        int(string)
        return True
    except ValueError:
        return False


def main():
    invalid, not_in_set, not_inset_cut, strange = verify_postal_codes("buenos-aires_argentina.osm")
    print(""" These are the obtained results when the verify_postal_codes function runs, these correspond to the 
          compilation of sets and lists that later are processed""")
    print("invalid_pc", invalid)
    print("not_in_set_pc", not_in_set)
    print("not_in_set_cut", not_inset_cut)
    print("strange_pc", strange)

if __name__ == '__main__':
    main()

