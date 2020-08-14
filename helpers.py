# coding: utf-8

import xml.etree.cElementTree as ET
from itertools import chain

def parse_xml_products(xml_raw_data):
    parsed_data = ET.fromstring(xml_raw_data)
    nodes = chain(parsed_data.findall('shop/offers/offer'))
    for node in nodes:
        yield dict(
            external_id=node.attrib["productId"],
            name=node.find('name').text,
            price=node.find('price').text,
            category_id=node.find('categoryId').text,
            article=node.find('xmlId').text,
            stocks=node.attrib["quantity"],
        )