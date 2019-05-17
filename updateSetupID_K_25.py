import xml.etree.ElementTree as ET
print 500000
tr = ET.parse("regional/GR_thessaly/GR_thessaly_setup_metrx_500000.xml")
for elem in tr.getroot():
    newid = int(elem.attrib.get('id')) + 500000
    elem.set('id', str(newid) )
tr.write("regional/GR_thessaly/GR_thessaly_setup_metrx_500000.xml")
