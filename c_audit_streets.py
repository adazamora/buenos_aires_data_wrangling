""" Audit street types"""

import xml.etree.cElementTree as ET
from collections import defaultdict
import re


OSMFILE = "buenos-aires_argentina.osm"
street_type_re = re.compile(r'^\S+\b', re.IGNORECASE)


def audit_streets(osmfile):
    """ Audits the street types encountered in the data

    Args:
        osmfile(xml file): from OpenStreetMap

    Returns:
        street_types(dict): a dictionary with the street type as keys and
        as a value a set of the entire street name where that type was encountered
    """
    with open(osmfile, "r", encoding="utf8") as osm_file:
        street_types = defaultdict(set)
        for event, elem in ET.iterparse(osm_file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
        # NOTE TO THE REVIEWER:
        # Please uncomment the code below if you want to see the different street types
        # for key, val in street_types.items():
        #     print(key, val)
    return street_types


def is_street_name(elem):
    """ Given a tag of a osm file, this returns a boolean that specifies if the node has a street attribute

    Args:
        elem(Element)
    Returns:
        bool: True if street attribute, False otherwise"""
    return elem.attrib['k'] == "addr:street"


def audit_street_type(street_types, street_name):
    """Returns the street type of a given street address.

    This code assumes that the street type is defined in the first word of the address

    Args:
    street_types(dict):  a dictionary of sets
    street_name(str): should be a string containing a street name from an osm file
    """
    first_word = street_type_re.search(street_name)
    if first_word:
        street_type = first_word.group()
        street_types[street_type].add(street_name)

st_types = audit_streets(OSMFILE)
