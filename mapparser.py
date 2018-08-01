#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint


def count_tags(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    taglist = []
    taglist.append(root.tag)
    for row in root:
        taglist.append(row.tag)
        for x in row:
            taglist.append(x.tag)
    tags = {}
    for i in taglist:
        tags[i] = taglist.count(i)
    return tags

def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    assert tags == {'bounds': 1,
                     'member': 3,
                     'nd': 4,
                     'node': 20,
                     'osm': 1,
                     'relation': 1,
                     'tag': 7,
                     'way': 1}

    

if __name__ == "__main__":
    test()
