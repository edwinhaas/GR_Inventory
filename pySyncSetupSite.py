import xml.etree.ElementTree as ET



setupTree = ET.parse("modifySetup.xml")
siteTree = ET.parse("modifySite.xml")

newSetup = ET.ElementTree(ET.Element("ldndcsetup"))
newSite  = ET.ElementTree(ET.Element("ldndcsite"))

#print len(setupTree.findall('.//setup'))

for elem in setupTree.getroot().findall('.//setup'):
    #print elem.tag, elem.get("id"),
    siteID = elem.find('use/site').get("id")
    #print siteID,
    for selem in  siteTree.getroot().findall('.//site'):
        if ( selem.get("id") == siteID ):
            #print " copied "
            ET.SubElement(newSetup.getroot(),elem)
            ET.SubElement(newSite.getroot(),selem)
            break
        #
    #
#

print ET.dump(setupTree)
#print ET.tostring(setupTree, encoding='utf8', method='xml')

