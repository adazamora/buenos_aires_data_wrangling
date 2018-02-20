import re
import xml.etree.cElementTree as ET
from c_audit_streets import is_street_name
from e_audit_postal_codes import get_postal_code, audit_postal_codes

STRANGEPC_DICT, INVALID_PC, NOT_IN_SET_PC = audit_postal_codes()

""" From the street types I obtained when I audited the streets (c_audit_streets) I selected the names 
    that are strange, here they are: 
    u'ALAMBRADO/PAREDON/LIMITE, Ferrocarril, Super, A, B, Esquina, Per, C, De, D, Audamérica, ' \
    u'SITIO, E, Grl, ING, Belgrano;25, Payr, 14c, Mir, RP, 624A, PASAJE, Jos, G, DE, H, ' \
    u'Humberto1。2357, Cno, DIP, Pres, PBRO, J, S, CMTE, Dragones, TGRL, Omb, avenida, Rep, M, BV, ' \
    u'Av.79, 76-Adelina, 361A, RCA, CJAL, O, Lista, F, Au, Av, P, D73, IGR, DIPUTADO, R, Pi, GDOR, ' \
    u'av, T, GRAL'
    
    Now I'm going to divide the strange names into MAPPING (names that are abbreviated and I'll change for other 
    names) and STREETS_TO_DELETE (names that are not streets and have a wrong tag)"""

MAPPING = {"CALLE": "Calle", "Avendida": "Avenida", "Av.": "Avenida", "AV": "Avenida", "avenida": "Avenida",
           "av": "Avenida", "RP": "Ruta Provincial", "Au": "Autopista",
           "PRES": "Presidente", "Pte": "Presidente", "Pres": "Presidente", "GDOR": "Gobernador",
           "Rep": "Republica", "GRL": "General", "GRAL": "General", "Grl": "General", "TTE": "Teniente",
           "TCNL": "Teniente Coronel", "Cno": "Camino", "DIP": "Diputado", "PBRO": "Presbítero",
           "SGT": "Sargento", "PJE": "Pasaje", "DR": "Doctor", "Dr": "Doctor", "CNL": "Coronel", "CMTE": "Comandante",
           "Audamérica": "Sudamérica", "P": "Pedro"}

STREETS_TO_DELETE = ["ALAMBRADO/PAREDON/LIMITE PROPIEDAD", "ING TTE DI TELLA", "Belgrano;25 de mayo"]

STREET_TYPE_RE = re.compile(r'^\S+\b', re.IGNORECASE)


def process_st_names_and_postalcodes():
    """ Process the street names and postal codes in a the Buenos Aires data osm file and returns an Element tree
    object"""
    process_st_tree = _improve_st_names("buenos-aires_argentina.osm".encode("utf-8"))
    return _clean_postal_codes(process_st_tree)


def _update_name(name):
    """ Updates the name of a street if the first word is in the MAPPING dictionary

    Args:
        name(str)
    Returns:
        updated_name(str): the updated name if the first word was in the MAPPING dictionary
    """
    first_word = STREET_TYPE_RE.search(name)
    if first_word:
        st_type = first_word.group()
        if st_type in MAPPING:
            expected_st = MAPPING[st_type]
            updated_name = re.sub(STREET_TYPE_RE, expected_st, name)
            return updated_name
    return


def _improve_st_names(osmfile):
    """ Changes the street names to a format given in MAPPING and deletes the streets that are not actually streets and
    have the street tag by mistake

    Args:
        osmfile
    Returns:
        tree(Element)
        """
    tree = ET.parse(osmfile)
    root = tree.getroot()
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if is_street_name(tag):
                    updatename = _update_name(tag.attrib['v'])
                    if updatename:
                        tag.set('v', updatename)
                    elif tag.attrib['v'] in STREETS_TO_DELETE:
                        root.remove(child)
    return tree


def _verify_replaced_streets(tree):
    """ Verifies if the street names were replaced correctly.

    Args:
    tree(Element): should be a tree that has been returned from _improve_st_names function"""
    root = tree.getroot()
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if is_street_name(tag) and _update_name(tag.attrib['v']):
                    print(u"This word was not replaced: ", tag.attrib)
    print("All words were replaced")


def _verify_deleted_nodes(tree):
    """ Verifies if the nodes were deleted correctly.

    Args:
    tree(Element): should be a tree that has been returned from _improve_st_names function
    """
    root = tree.getroot()
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if tag.attrib['v'] in STREETS_TO_DELETE:
                    print(u"This node was not deleted: ", tag.attrib)
    print("All nodes were deleted")


""" POSTAL CODES """


def _clean_postal_codes(tree):
    """ Deletes the node of the postal codes that are incorrect and changes the postal codes that are do exist
    but are not written correctly in the osm file

    Args:
        tree(Element)
    Returns:
        tree(Element)
    """
    root = tree.getroot()
    for child in root:
        if child.tag == "node":
            for tag in child.iter("tag"):
                if get_postal_code(tag):
                    p_code = tag.attrib['v']
                    if p_code in STRANGEPC_DICT:
                        tag.set('v', STRANGEPC_DICT[p_code])
                    elif p_code in INVALID_PC or p_code in NOT_IN_SET_PC:
                        child.remove(tag)
    return tree


def _verify_postal_codes(tree):
    """ Verifies if the postal codes were deleted and replaced correctly.

    Args:
        tree(Element): should be a tree that has been returned from the _clean_postal_codes function
        """
    root = tree.getroot()
    for child in root:
        if child.tag == "node":
            for tag in child.iter("tag"):
                if get_postal_code(tag):
                    p_code = tag.attrib['v']
                    if p_code in STRANGEPC_DICT:
                        if p_code != '1776':
                            print(u"This post code was not replaced: ", tag.attrib)
                    elif p_code in INVALID_PC or p_code in NOT_IN_SET_PC:
                        print(u"This post code was not deleted: ", tag.attrib)
    print("All postal codes were replaced/deleted")


def main():
    validate_tree = process_st_names_and_postalcodes()
    _verify_replaced_streets(validate_tree)
    _verify_deleted_nodes(validate_tree)
    _verify_postal_codes(validate_tree)

if __name__ == '__main__':
    main()
