import xml.etree.ElementTree as ET
import pandas as pd

thessy = pd.read_csv("grid-ids-thessaly.txt", sep='\t')

ids = thessy['NCU_NR']
print ids

tree = ET.parse('bio11/regional/GR_arable/GR_arable_setup.xml')
root = tree.getroot()
for child in root.getchildren():
    id = child.attrib["id"]
    print id
    #continue
    check = (ids == int(id))
    
    if (check.any() ):
        print "keep " , child.tag, child.attrib, len(root.getchildren())
    else: 
        print "remove " , child.tag, child.attrib, len(root.getchildren())
        root.remove(child)
    #
#
new = ET.ElementTree(root)
print len(root.getchildren())
new.write("GR_setup_new.xml")

