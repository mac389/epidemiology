'''
http://catalog.data.gov/api/3/
'''
import requests
from xml.etree import ElementTree
from lxml import etree


request_params_open = """<?xml version="1.0" encoding="utf-8"?>
<request-parameters>
<parameter>
<name>accept_datause_restrictions</name>
<value>true</value>
</parameter>"""

request_parapms_close = "</request-parameters>"

xml_request = request_params_open + """<parameter><name>B_1</name>
<value>D76.V1-level1</value>
</parameter>"""+request_parapms_close
print xml_request
base_url = "https://wonder.cdc.gov/controller/datarequest"
r = requests.post(base_url, data={"request_xml":xml_request})

print r.content
tree = ElementTree.fromstring(r.content)
print tree