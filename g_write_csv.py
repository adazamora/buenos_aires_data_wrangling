#!/usr/bin/env python
# -*- coding: utf-8 -*-

from f_clean_osm_data import process_st_names_and_postalcodes
import unicodecsv as csv
import codecs
import pprint
import re
import cerberus
import schema

cleaned_data_tree = process_st_names_and_postalcodes()
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Making sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


# Part of my code

def find_colons(input_string):
    """ Finds a colon in a string"""
    return [x.start() for x in re.finditer('\:', input_string)]


def create_nodes(element, node_fields, node_tags_fields, now):
    """ Creates nodes to be exported then to a csv file.

    Args:
        element(Element)
        node_fields(list): containing the nodes fields in the correct order
        node_tags_fields(list): containing the nodes tags fields in the correct order
        now(str): defining if a node or a way is being created

    Returns:
        node_dict(dict)
        """
    node_dict = {now: {}}
    for f in node_fields:
        node_dict[now][f] = element.attrib[f]
    node_dict[now + '_tags'] = []
    root_attr = element.attrib
    for child in element:
        if child.tag == 'tag':
            child_attr = child.attrib
            k = child_attr['k']
            if PROBLEMCHARS.search(k) is None:
                tag_fields = {}
                colons_positions = find_colons(k)
                if len(colons_positions) >= 1:
                    tag_fields['type'] = k[:colons_positions[0]]
                    tag_fields['key'] = k[colons_positions[0] + 1:]
                else:
                    tag_fields['type'] = 'regular'
                    tag_fields['key'] = k
                tag_fields['value'] = child_attr['v']
                tag_fields['id'] = root_attr['id']
            node_dict[now + '_tags'].append(tag_fields)
    return node_dict


def create_ways(element, way_fields, way_tags_fields, now):
    """ Creates ways to be exported then to a csv file.

    Args:
        element(Element)
        node_fields(list): containing the ways fields in the correct order
        node_tags_fields(list): containing the ways tags fields in the correct order
        now(str): defining if a node or a way is being created

    Returns:
        ways_dict(dict)
    """
    ways_dict = create_nodes(element, way_fields, way_tags_fields, now)

    ways_dict['way_nodes'] = []
    root_attr = element.attrib
    counter = 0
    for child in element:
        if child.tag == 'nd':
            child_attr = child.attrib
            tag_fields = {}
            tag_fields['id'] = root_attr['id']
            tag_fields['node_id'] = child_attr['ref']
            tag_fields['position'] = counter
            ways_dict['way_nodes'].append(tag_fields)
            counter += 1
    return ways_dict


""" The code below was provided by Udacity - Case Study: OpenStreetMap data (SQL)"""


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    if element.tag == 'node':
        return create_nodes(element, NODE_FIELDS, NODE_TAGS_FIELDS, 'node')
    elif element.tag == 'way':
        return create_ways(element, WAY_FIELDS, WAY_TAGS_FIELDS, 'way')


""" The code below was provided by Udacity - Case Study: OpenStreetMap data (SQL)"""
# ================================================== #
#               Helper Functions                     #
# ================================================== #

def get_element(input_tree, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""
    root = input_tree.getroot()
    for child in root:
        if child.tag in tags:
            yield child


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, str) else v) for k, v in row.items()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


""" Part of the code below was provided by Udacity - Case Study: OpenStreetMap data (SQL)"""

# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(input_tree, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'wb') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'wb') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(input_tree, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(cleaned_data_tree, validate=False)
    # process_map("small_sample.osm", validate=True)