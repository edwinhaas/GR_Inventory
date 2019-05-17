#/bin/python

import pandas as pd

textfilein = "cells_1500.csv"
rotations = 5
SCmodule = 'metrx'

'''FID;TARGET_FID;GRIDCODE;NUTS;SGDB;NCU_NR;AREA;NUTS_E;COUNTRY;SGDB_E;ORIG_FID;Id;Input_FID;Station_na;Station_el;Region;Height;Y;X'''

'''<?xml version="1.0"?>
 <ldndcsetup>
'''
setup = ''' <setup id="%s" model="%s" LandUse="%s" Area="%s" CStation="%s" >
   <location latitude="%s" longitude="%s" elevation="%s" />
   <mobile>
    <modulelist>
     <module id="microclimate:canopyecm" timemode="daily" />
     <module id="microclimate:dndc" timemode="daily" />
     <module id="watercycle:dndc" timemode="daily" />
     <module id="airchemistry:depositiondndc" timemode="daily"/>
     <module id="physiology:dndc" timemode="daily" />
     <module id="physiology:grasslanddndc" timemode="daily" />
     <module id="soilchemistry:%s" timemode="daily" />
     <module id="output:physiology:daily"  />
     <module id="output:soilchemistry:daily"  />
     <module id="output:soilchemistry:yearly" />
     <module id="output:watercycle:daily"  />
     <module id="output:report:arable" timemode="daily" />
    </modulelist>
   </mobile>
   <use>
    <climate id="%s" />
    <event id="%s" />
    <site id="%s" />
   </use>
  </setup>
'''


alldata = pd.read_csv(textfilein, sep=';')
sitedata = pd.read_csv("ids.txt", sep='\t',header=0,index_col=False)
#print sitedata


out = []
i = 0
out.append('<?xml version="1.0"?>\n <ldndcsetup>\n')
for r in range(1,rotations+1):
    offset = r * 100000
    print "rotation: ", r
    for index, row in alldata.iterrows():
        print index,row["NCU_NR"]
        ncuid = row["NCU_NR"]
        if ( ncuid in set(sitedata["siteid"]) ):
            print "ncuid " , ncuid , " in siteid, processing..."
        else:
            print "ncuid " ,  ncuid , " not in siteid, skip"
            continue
        #
        #setupTXT = setup % ( str(row["cellid"]) , row["kernel"]) , row["kernelmodel"]) , str(row["area"])) , str(row["climate"])), str(row["event"])), str(row["site"]))   )
        setupTXT = setup % ( str(offset+row["FID"]) , "mobile" , "arable" , str(row["AREA"]) , str(row["Station_el"]), str(row["X"]),str(row["Y"]),str(row["Height"]),SCmodule, str(row["Station_na"]), str(r), str(row["NCU_NR"]) )
        i = i+ 1
        #print setupTXT
        #exit(1)
        out.append(setupTXT)
    #endfor
#endif
out.append('</ldndcsetup>\n')

#print out

print
print " processed ", i , "datasets"
print

text_file = open("GR_thessaly_setup.xml", "w")
text_file.write("\n".join(out))
text_file.close()





