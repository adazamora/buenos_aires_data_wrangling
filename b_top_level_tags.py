""" Top level tags in the document """

import xml.etree.cElementTree as ET
from collections import defaultdict


def count_tags(filename):
    tags = defaultdict(int)
    for event, element in ET.iterparse(filename):
        tags[element.tag] += 1
    return tags

print(count_tags('buenos-aires_argentina.osm'))