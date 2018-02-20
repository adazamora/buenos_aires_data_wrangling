import xml.etree.cElementTree as ET

""" As the original data file is approximately 33KB, I will write two samples of the data to work with:
1. A small sample (about 1/50 the original data size) to verify that my code is working correctly
2. A medium sample (about 1/3 of the original data size) to run my code"""


""" This code was provided by Udacity https://classroom.udacity.com/nanodegrees/nd002/parts/
860b269a-d0b0-4f0c-8f3d-ab08865d43bf/modules/316820862075463/lessons/3168208620239847/concepts/77135319070923"""


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def write_sample_data(osm_file, sample_file, k_parameter):
    """ osm_file refers to an xml file name, sample_file is the file output name
    k_parameter is a parameter that takes every k-th top level element"""

    with open(sample_file, 'wb') as output:
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode())
        output.write('<osm>\n  '.encode())

        # Write every kth top level element
        for i, element in enumerate(get_element(osm_file)):
            if i % k_parameter == 0:
                output.write(ET.tostring(element, encoding='utf-8'))
        output.write('</osm>'.encode())

# Writing a small sample file, which will be used later to verify the code:

write_sample_data('buenos-aires_argentina.osm', 'small_sample.osm', 50)

# Writing a medium sample file, which will be used later to verify the code:

write_sample_data('buenos-aires_argentina.osm', 'med_sample.osm', 3)