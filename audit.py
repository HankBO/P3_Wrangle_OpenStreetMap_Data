"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "san-antonio_texas.osm"
SAMPLE_FILE = "sample_sa.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Path"]

mapping = { 
            "Rd": "Road",
            "St": "Street",
            "Ave":"Avenue",
            "Hwy":"Highway",
            "Hiwy":"Highway",
            "W"  : "West",
            "N"  : "North",
            "E"  : "East",
            "S"  : "South"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    words = name.split()
    for w in range(len(words)):
        if words[w] in mapping:
            if words[w-1].lower() not in ['avenue']:
                words[w] = mapping[words[w]]
                name = " ".join(words)
    return name

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode" or elem.attrib['k'] == "postal_code")

def audit_postcode(osmfile):
    osm_file = open(osmfile, "r")
    postcode = []
    for _, element in ET.iterparse(osm_file):
        if element.tag == "node" or element.tag == "way" or element.tag == "relation":
            for tag in element.iter("tag"):
                if is_postcode(tag):
                    postcode.append(tag.attrib['v'])
    osm_file.close()
    return postcode

def update_postcode(ele):
    if ele.find("-")  != -1:
        ele = ele[0:5]
    elif ele[0:2] == "TX":
        ele = ele[-5:]
    return ele   

postcode = audit_postcode(SAMPLE_FILE)
for ele in postcode:
    pc_fix = update_postcode(ele)
    print ele, "=>", pc_fix

def test():
    st_types = audit(SAMPLEFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name


if __name__ == '__main__':
    test()