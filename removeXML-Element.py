import xml.etree.ElementTree as ET
tr = ET.parse("GR_site.xml")
for elem in tr.getroot():
    if elem.attrib.get('countryid') != "GR":
        print elem.tag, elem.attrib
        tr.getroot().remove(elem)

tr.write("GR_site.xml")
