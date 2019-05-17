#/bin/python
#
#
#
import csv
import pandas as pd
import datetime as dt
import sys


# Scenario Irrigation
#scenario = "rainfed"
#scenario = "irri"

scenario = sys.argv[1]

if ( (scenario != "rainfed") and (scenario != "irri")):
    print "error, rainfed or irri is missing"
    exit(1)
#
yearStart = 2009
years = 7
rotations = 5
cropType = {'sico':'crop','wbar':'crop','wiwh':'crop','cott':'crop','perg':'grass' }
cropInitBiomass = {'sico':100,'wbar':100,'wiwh':100,'cott':200,'perg':200 }
cropOptYield = {'sico':5000,'wbar':4000,'wiwh':6000,'cott':6000,'perg':4000 }
cropMaxTDD = {'sico':3400,'wbar':2500,'wiwh':2300,'cott':3300,'perg':6000 }
cropWinterlimit = {'sico':-99.99,'wbar':400,'wiwh':400,'cott':-99.99,'perg':400 }
cropTLimit = {'sico':7,'wbar':8,'wiwh':8,'cott':7,'perg':7 }
cropIniNfix = {'sico':-99.99,'wbar':-99.99,'wiwh':-99.99,'cott':-99.99,'perg':0.9 }

print cropType
print cropInitBiomass
print

startYear = 2010

# File with crop properties
# DF is a pandas Dataframe
#DFinputCrops = pd.read_csv("GR_thess_crop.csv", sep='\t', index_col=0).fillna('NaN')
#DFinputCrops = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="ROT",index_col=0, usecols="B:L", skiprows=1, skipfooter=28 ).fillna('NaN')
DFinputCrops = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="Dates",index_col=0, usecols="A:F", dtype={'Crop':str, 'sico':str, 'wiwh':str, 'perg':str, 'cott':str, 'wbar':str}).fillna('nan')
print DFinputCrops

dictFert = {}
crops = ['sico','wbar','wiwh','cott','perg']

for crop in crops :
    print "Fert: " , crop,
    fertilize = []
    fertd = DFinputCrops.get_value('Ferti1_date',crop)[:10]
    fertr = DFinputCrops.get_value('Fert1_%',crop)
    print fertd, fertr,
    if ((fertd != 'nan') and (fertr > 0.0)) : fertilize.append([fertd,fertr])
    fertd = DFinputCrops.get_value('Fert2_date',crop)[:10]
    fertr = DFinputCrops.get_value('Ferti2_%',crop)
    print fertd, fertr,
    if ((fertd != 'nan') and (fertr > 0.0)) : fertilize.append([fertd,fertr])
    fertd = DFinputCrops.get_value('Fert3_date',crop)[:10]
    fertr = DFinputCrops.get_value('Fert3_%',crop)
    print fertd, fertr
    if ((fertd != 'nan') and (fertr > 0.0)) : fertilize.append([fertd,fertr])
    dictFert[crop]=fertilize
#

dictManure = {}

for crop in crops :
    print "Manure: " , crop,
    manure = []
    manurd = DFinputCrops.get_value('Manure1_date',crop)[:10]
    manurr = DFinputCrops.get_value('Manure1_rate',crop)
    print manurd, manurr,
    if ((manurd != 'nan') and (manurr > 0.0)) :
        manure.append([manurd,manurr])
    manurd = DFinputCrops.get_value('Manure2_date',crop)[:10]
    manurr = DFinputCrops.get_value('Manure2_rate',crop)
    print manurd, manurr,
    if ((manurd != 'nan') and (manurr > 0.0)) :
        manure.append([manurd,manurr])
    manurd = DFinputCrops.get_value('Manure3_date',crop)[:10]
    manurr = DFinputCrops.get_value('Manure3_rate',crop)
    print manurd, manurr
    if ((manurd != 'nan') and (manurr > 0.0)) :
        manure.append([manurd,manurr])
    dictManure[crop]= manure
#

dictCut = {}
#cutcrops = ['alfa', 'alfalfa1', 'alfalfa2']
cutcrops = ['perg']
for crop in cutcrops :
    cut = []
    cutd = DFinputCrops.get_value('Cut1_date',crop)[:10]
    if (cutd != 'nan' ) :
        cut.append(cutd)
    dictCut[crop]= cut
    cutd = DFinputCrops.get_value('Cut2_date',crop)[:10]
    if (cutd != 'nan' ) :
        cut.append(cutd)
    dictCut[crop]= cut
    cutd = DFinputCrops.get_value('Cut3_date',crop)[:10]
    if (cutd != 'nan' ) :
        cut.append(cutd)
    dictCut[crop]= cut
    cutd = DFinputCrops.get_value('Cut4_date',crop)[:10]
    if (cutd != 'nan' ) :
        cut.append(cutd)
    dictCut[crop]= cut
    cutd = DFinputCrops.get_value('Cut5_date',crop)[:10]
    if (cutd != 'nan' ) :
        cut.append(cutd)
    dictCut[crop]= cut
#

# Irrigation
dictIrri = {}
for crop in crops :
    irri = []
    #Irri1_date        12.3.2016
    #Irri1_quan
    for d in range(1,19) :
        irriDate = "Irri" + str(d) + "_date"
        irriQuan = "Irri" + str(d) + "_quan"
        irrid = DFinputCrops.get_value(irriDate,crop)[:10]
        irriq = DFinputCrops.get_value(irriQuan,crop)
        if ((irrid != 'nan') and (irriq > 0.0) ) :
            irri.append([irrid, irriq])
    dictIrri[crop]= irri
#

dictPlant = {}
dictHarvest = {}
for crop in crops :
    pDate = DFinputCrops.get_value('Seeding',crop)[:10]
    Yield = DFinputCrops.get_value('Yield',crop)
    tdd = DFinputCrops.get_value('temp degree sum',crop)
    hDate = DFinputCrops.get_value('Harvest',crop)[:10]
    Residues = DFinputCrops.get_value('Residues',crop)
    dictPlant[crop]=[pDate, Yield, tdd]
    dictHarvest[crop]=[hDate,Residues]
#

print "Fert ", dictFert
print "Manu ", dictManure
print "Cut  ", dictCut
print "Irri ", dictIrri
print "Plant", dictPlant
print "Harvest", dictHarvest


#DFinputFertIrri = pd.read_csv("GR_thess_fert_irri.csv", sep='\t', index_col=0).fillna('NaN')
DFinputFertIrri = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="ROT",index_col=0, usecols="B:L", skiprows=1, skipfooter=28 )
print DFinputFertIrri
#DFinputFertRainfeed = pd.read_csv("GR_thess_fert_rainfeed.csv", sep='\t', index_col=0).fillna('NaN')
DFinputFertRainfeed = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="ROT",index_col=0, usecols="B:L", skiprows=10, skipfooter=19 )
print DFinputFertRainfeed

#DFinputManureIrri = pd.read_csv("GR_thess_manure_irri.csv", sep='\t', index_col=0).fillna('NaN')
DFinputManureIrri = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="ROT",index_col=0, usecols="B:L", skiprows=20, skipfooter=9 )
print DFinputManureIrri
#DFinputManureRainfeed = pd.read_csv("GR_thess_manure_rainfeed.csv", sep='\t', index_col=0).fillna('NaN')
DFinputManureRainfeed = pd.read_excel("Management-Input-Data_v4.xlsx",sheet_name="ROT",index_col=0, usecols="B:L", skiprows=29, skipfooter=0 )
print DFinputManureRainfeed
print
#print DFinputFertIrri.loc[2010:2010]['R1rate']
#print DFinputFertIrri.get_value(2010,'R1rate')


XMLheader = '''<?xml version="1.0"?>
<ldndcevent>
  <global time="2009-01-01" />
'''
XMLevent = '''  <event  id="%s" >
    <global time="2009-01-01" />\n'''
XMLplant = '''    <event type="plant" time="%s" >
      <plant name="%s" type="%s" >
        <crop initialbiomass="%s"  />
        <params>
          <par name="max_tdd" value="%.1f" />
          <par name="optyield" value="%.1f" />
          <par name="ini_n_fix" value="%.2f" />
          <par name="winterlimit" value="%.2f" />
          <par name="tlimit" value="%.2f" />
        </params>
      </plant>
    </event>\n'''
XMLplantGrass = '''    <event type="plant" time="%s" >
      <plant name="%s" type="%s" >
        <grass initialbiomass="%s"  />
        <params>
          <par name="max_tdd" value="%.1f" />
          <par name="optyield" value="%.1f" />
          <par name="ini_n_fix" value="%.2f" />
          <par name="winterlimit" value="%.2f" />
          <par name="tlimit" value="%.1f" />
        </params>
      </plant>
    </event>\n'''
XMLharvest = '''    <event  type="harvest" time="%s" >
      <harvest  name="%s" remains="%s" />
    </event>\n'''
XMLfertilize = '''    <event  type="fertilize" time="%s" >
      <fertilize  type="nh4so4" amount="%6.2f" depth="0.05" />
    </event>\n'''
XMLmanure = '''    <event type="manure" time="%s" >
      <manure type="slurry" ph="7.61" c="%5.2f" cn="8.8" availn="0.68" nh4fraction="0.71" donfraction="0.06" no3fraction="0.0" ureafraction="0.23" cellulosefraction="0.6" ligninfraction="0.2" availc = "0.1" />
    </event>\n'''
XMLirrigate = '''    <event type="irrigate" time="%s">
      <irrigate amount="%5.2f" ph="7.0"/>
    </event>\n'''
XMLcut = '''    <event type="cut" time="%s" >
      <cut remains="100.000" />
    </event>\n'''
XMLeventEnd = '''  </event>\n'''
XMLFooter = '''</ldndcevent>\n\n'''


fout = open('mana_'+scenario+'.xml','w')

outString = []
outText = []
outString= XMLheader
fout.write(outString)
previousCrop = 0
previousCropName = ''
previousCropRemains = 0.0
cropName = ''
# Rotation
print
print "Rotations "
print
for rot in range(1,rotations+1):
    print "Rotation: ", rot
    Rcrop = "R"+str(rot)+"crop"
    Rrate = "R"+str(rot)+"rate"
    #
    outString = XMLevent % rot
    fout.write(outString)
    # Year
    previousCropName = ''
    cropName = ''
    for y in range(yearStart,yearStart+years+1):
        print "\t - Year: " , y ,
        outString = '<!-- ' + str(y) + '-->\n'
        fout.write(outString)
        if y == yearStart:
            print
            continue
        #
        previousCropName = cropName
        if scenario == "irri":
            cropName = DFinputFertIrri.get_value(y,Rcrop)
        else:
            cropName = DFinputFertRainfeed.get_value(y,Rcrop)
        #
        print "Crop: ", cropName, previousCropName
        # Harvest previous Crop ?
        if (previousCrop):
            # Harvest previous crop
            outString = XMLharvest % ( '2010-04-01', previousCropName , previousCropRemains)
            fout.write(outString)
            previousCrop = 0
        #
        # Fertilize crop
        #
        if scenario == "irri":
            fertRate = DFinputFertIrri.get_value(y,Rrate)
        else:
            fertRate = DFinputFertRainfeed.get_value(y,Rrate)
        #
        #print "fertRate" , fertRate
        #
        if (fertRate > 0.0 ):
            print "Fert: ",fertRate, " Appl. ", len(dictFert[cropName]),
            for app in range(0,len(dictFert[cropName])) :
                if ( dictFert[cropName][app][0] != 'nan' ):
                    fertDate = str(y) + dictFert[cropName][app][0][4:]
                    fertQuant = dictFert[cropName][app][1]
                    outString = XMLfertilize % ( fertDate, (float(fertQuant) / 100.0 * fertRate ))
                    fout.write(outString)
                #
            #
        #
        if scenario == "irri":
            manureRate = DFinputManureIrri.get_value(y,Rrate)
        else:
            manureRate = DFinputManureRainfeed.get_value(y,Rrate)
        #
        if (manureRate > 0.0 ):
            print "Manure: ",manureRate," Appl. ", len(dictManure[cropName]),
            c = float(manureRate) * 8.8
            for app in range(0,len(dictManure[cropName])) :
                if ( dictManure[cropName][app][0] != 'nan'):
                    manureDate = str(y) + dictManure[cropName][app][0][4:]
                    manureQuant = dictManure[cropName][app][1]
                    outString = XMLmanure % ( manureDate, (float(manureQuant) / 100.0 * c ) )
                    fout.write(outString)
                #
            #
        #
        if ( dictPlant[cropName][0] != 'nan' ):
            # Plant next crop
            if (cropName == "perg" and previousCropName == "perg") :
                print "no planting this year ",
            else:
                if ( cropName == "WIWH" or cropName == "wiwh" or cropName == "winterwheat" or cropName == "WBAR" or cropName == "wbar" or cropName == "winterbarley" or cropName == "perg" or cropName == "PERG" ) :
                    plantdatestring = str(y-1) + dictPlant[cropName][0][4:]
                    print "wintercrop " ,
                else:
                    plantdatestring = str(y) + dictPlant[cropName][0][4:]
                #endif
                print "Planting ", plantdatestring,
                #print plantdatestring
                if ( cropName == "perg" or cropName == "perg1" or cropName == "perg2") :
                    outString = XMLplantGrass % ( plantdatestring, cropName , cropName, cropInitBiomass[cropName], cropMaxTDD[cropName], cropOptYield[cropName], cropIniNfix[cropName], cropWinterlimit[cropName], cropTLimit[cropName])
                else:
                    outString = XMLplant % ( plantdatestring, cropName , cropName, cropInitBiomass[cropName], cropMaxTDD[cropName], cropOptYield[cropName], cropIniNfix[cropName], cropWinterlimit[cropName], cropTLimit[cropName])
                #endif
                fout.write(outString)
            #endif alfalfa2
        if ( dictHarvest[cropName][0] != 'nan' ):
            if ( (cropName == "perg") and (previousCropName != "perg") and (previousCropName != "")) :
                print "no harvest this year ",
            else:
                if ( cropName == "perg" ) :
                    harvestdatestring = str(y+1) + dictHarvest[cropName][0][4:]
                else:
                    harvestdatestring = str(y) + dictHarvest[cropName][0][4:]
                #
                remains = 1.0
                print "Harvest ", harvestdatestring,
                outString = XMLharvest % ( harvestdatestring, cropName , dictHarvest[cropName][1])
                fout.write(outString)
                #print "Irri. Appl. ", len(dictIrri['perg']),
                #for app in range(0,len(dictIrri['perg'])) :
                #    if ( dictIrri['perg'][app][0] != 'NaN' ):
                #        irriDate = str(y) + dictIrri['perg'][app][0][4:]
                #        irriQuant = dictIrri['perg'][app][1]
                #        outString = XMLirrigate % ( irriDate, irriQuant )
                #        fout.write(outString)
                #    #
                ##
                #print "Cut ", len(dictCut['perg']),
                #for cut in range(0,len(dictCut['perg'])) :
                #    if ( dictCut['perg'][cut] != 'NaN' ):
                #        cutDate = str(y) + dictCut['perg'][cut][4:]
                #        outString = XMLcut % ( cutDate )
                #        fout.write(outString)
                #     #endif
                ##endfor
            #endif perg
            #if ( cropName == "wbar" ) :
            #    print "adding perg after wbar for cover crop ",
            #    #print str(y) , dictPlant['perg1'][0][4:]
            #    plantdatestring = str(y) + dictPlant['perg'][0][4:]
            #    print "Planting ", plantdatestring,
            #    #print plantdatestring
            #    outString = XMLplantGrass % ( plantdatestring, 'perg' , 'perg', cropInitBiomass['perg'])
            #    fout.write(outString)
            #    harvestdatestring = str(y+1) + dictHarvest['perg'][0][4:]
            #    print "Harvest ", harvestdatestring,
            #    outString = XMLharvest % ( harvestdatestring, 'perg' , dictHarvest['perg'])
            #    fout.write(outString)
            # #endif
        # Manure crop, basal and after harvest
        # Irrigation
        if ((scenario == "irri") and (len(dictIrri[cropName]) > 0) ):
            print "Irri. Appl. ", len(dictIrri[cropName]),
            for app in range(0,len(dictIrri[cropName])) :
                if ( dictIrri[cropName][app][0] != 'nan' ):
                    irriDate = str(y) + dictIrri[cropName][app][0][4:]
                    irriQuant = dictIrri[cropName][app][1]
                    outString = XMLirrigate % ( irriDate, float(irriQuant) )
                    fout.write(outString)
                #
            #
        #
        # Cutting Feed crops
        if (cropName in ['perg', 'alfa', 'alfalfa2'] and len(dictCut[cropName]) > 0 ) :
            print "Cut ", len(dictCut[cropName]),
            for cut in range(0,len(dictCut[cropName])) :
                if ( dictCut[cropName][cut] != 'nan' ):
                    cutDate = str(y) + dictCut[cropName][cut][4:]
                    outString = XMLcut % ( cutDate )
                    fout.write(outString)
                #endif
            #endfor
            # Cuts for the next year until grass is removed
            #for cut in range(0,len(dictCut['perg'])) :
            #    if ( dictCut['perg'][cut] != 'NaN' ):
            #        cutDate = str(y+1) + dictCut['perg'][cut][4:]
            #        outString = XMLcut % ( cutDate )
            #        fout.write(outString)
            #                #endif
            ##endfor

        #endif
        print
    #
    previousCropName = cropName
    outString = XMLeventEnd
    fout.write(outString)
#
outString=XMLFooter
fout.write(outString)
fout.close()




