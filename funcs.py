import os
import sys
import xml.etree.ElementTree as ET
import urllib, urllib2
from string import Template

#helper function to strip namespace
def getElementTag(element):
	eTag = element.tag.split("}")[1]
	return eTag

def getElementNS(element):
	eNS = element.tag.split("}")[0] + "}"
	return eNS

# function to generate full paths
def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

#function to download all records from a set, write to files for each 100 batch (e.g. publication:psychfrp100.xml, publication:psychfrp200.xml)
def getSetRecords(setID,baseOAI):
	print "Getting",setID,"..."
	filesafeSetID = setID.split(":")[1]

	resumpTokensGo = True
	
	#initial query to set token
	initialSetURL = "{baseOAI}verb=ListRecords&set={setID}&metadataPrefix=oai_dc".format(setID=setID,baseOAI=baseOAI)
	setXML = urllib2.urlopen(initialSetURL)
	contents = setXML.read()
	file = open("./setsXML/"+filesafeSetID+"_100.xml", 'w')
	file.write(contents)
	file.close()
	print ("./setsXML/"+filesafeSetID+"_100.xml written")

	#read initial set, if resumptive token, iterate through until all records swooped up
	root = ET.parse("./setsXML/"+filesafeSetID+"_100.xml").getroot()
	rootTag = getElementTag(root)
	rootNS = getElementNS(root)
	resumpTokenCheck = root.findall(rootNS+"ListRecords/"+rootNS+"resumptionToken")	

	#if resumption token present
	if len(resumpTokenCheck) > 0:
		tokenCount = 200
		#iterate through all batches
		while resumpTokensGo == True:				
			resumpToken = resumpTokenCheck[0].text		
			tokenizedSetURL = "{baseOAI}verb=ListRecords&resumptionToken={resumpToken}".format(resumpToken=resumpToken,baseOAI=baseOAI)
			setXML = urllib2.urlopen(tokenizedSetURL)
			
			#set filename
			filename = "./setsXML/"+setID+"_"+str(tokenCount)+".xml"

			contents = setXML.read()
			file = open(str(filename), 'w')
			file.write(contents)
			file.close()
			print(str(filename)+" written")

			#check for more batches
			root = ET.parse(str(filename)).getroot()
			rootTag = getElementTag(root)
			rootNS = getElementNS(root)
			resumpTokenCheck = root.findall(rootNS+"ListRecords/"+rootNS+"resumptionToken")
			# print "Text of resumpTokenCheck is:",resumpTokenCheck[0].text	

			if resumpTokenCheck[0].text == "None":
				tokenCount = tokenCount + 100
				continue
			else:
				print setID,"complete."
				#conditional to set resumpTokensGo to false
				resumpTokensGo = False

#function to download OAI sets
def downloadOAI(baseOAI):
	#get ListSets
	setsURL = baseOAI + "verb=ListSets"
	setsRoot = ET.parse(urllib.urlopen(setsURL)).getroot()
	rootTag = getElementTag(setsRoot)
	rootNS = getElementNS(setsRoot)

	#get setSpecs
	setSpecs = []
	setSpecsTemp = setsRoot.findall(rootNS+"ListSets/"+rootNS+"set/"+rootNS+"setSpec")
	#remove subsets (e.g. dissertations from ProQuest)
	for set in setSpecsTemp:
		
		# removes WSU dissertations and theses, as depostied by the Library
		# if not set.text.endswith('theses') and not set.text.endswith('diss'):
		
		# removes WSU dissertations and theses, as depostied by ProQuest
		if not set.text.endswith('dissertations'):		
			setSpecs.append(set.text)

	#get setsXML
	for set in setSpecs:
		getSetRecords(set,baseOAI)
		print set,"done."
	print "All sets downloaded."

#function to transform downloaded OAI xml into Solr ready XML
def transformFiles(saxonLocation):
	#transform OAI XML to Solr indexing XML
	fileList = listdir_fullpath('./setsXML')		
	for file in fileList:
		outputFile = "." + file.split(".")[1] + "_Solr.xml"
		cs = 'java -jar {saxonLocation} -s:{file} -xsl:dc2solr.xsl -o:{outputFile}'.format(file=file, outputFile=outputFile, saxonLocation=saxonLocation)		
		try:			
			os.system(cs)
			print file,"processed."			
		except:
			#this should include a logging event
			print file,"had errors and did NOT process."

	#move all files to solrXML
	os.system("mv ./setsXML/*_Solr.xml ./solrXML/")


#index Solr ready XML into Solr
def indexSolr(baseURL):	
	#index in Solr
	fileList = listdir_fullpath('./solrXML')
	for file in fileList:			
		os.system("curl -v '{baseURL}/update/?commit=true' --data-binary @{file} -H 'Content-type:text/xml; charset=utf-8'".format(file=file, baseURL=baseURL))





