""" Audit coordinates"""

import xml.etree.cElementTree as ET


def check_coordinates(osmfile):
    """ Checks if the coordinates of an osm file are within the Buenos Aires province area

        Args:
        osmfile(xml file): from OpenStreetMap"""
    tree = ET.parse(osmfile)
    root = tree.getroot()
    # All of the below min and max values where manually selected by me using Google maps
    min_lat = -41.06
    max_lat = -33.31
    min_lon = -63.43
    max_lon = -56.77
    for child in root:
        if child.tag == "node":
            latitude = float(child.attrib["lat"])
            longitude = float(child.attrib["lon"])
            if latitude > max_lat or latitude < min_lat or longitude > max_lon or longitude < min_lon:
                print("latitude", latitude)
                print("longitude", longitude)
    print("All coordinates are ok")


check_coordinates("buenos-aires_argentina.osm")
