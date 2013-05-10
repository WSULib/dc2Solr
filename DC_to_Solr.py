#utility designed to pull records from DC@WSU, via OAI, and index them in Solr
#imports done by funcs.py
import os
import sys
import xml.etree.ElementTree as ET
import urllib, urllib2
from string import Template
import time
#workhorse functions for this utility in funcs.py
import funcs

#global vars
baseURL = "http://localhost/solr4/mods"

def downloadOAI():
	#get ListSets
	setsURL = "http://digitalcommons.wayne.edu/do/oai/?verb=ListSets"
	setsRoot = ET.parse(urllib.urlopen(setsURL)).getroot()
	rootTag = funcs.getElementTag(setsRoot)
	rootNS = funcs.getElementNS(setsRoot)

	#get setSpecs
	setSpecs = []
	setSpecsTemp = setsRoot.findall(rootNS+"ListSets/"+rootNS+"set/"+rootNS+"setSpec")
	#if don't end in "theses" or "diss", add them to list
	for set in setSpecsTemp:
		if not set.text.endswith('theses') and not set.text.endswith('diss'):		
			setSpecs.append(set.text)

	#get setsXML
	for set in setSpecs:
		funcs.getSetRecords(set)
		print set,"done."
	print "All sets - non Theses and Dissertations - downloaded."

def transformFiles():
	#transform OAI XML to Solr indexing XML
	fileList = funcs.listdir_fullpath('./setsXML')		
	for file in fileList:
		outputFile = "." + file.split(".")[1] + "_Solr.xml"
		cs = Template('java -jar /var/opt/fedora_utilities/saxon9he.jar -s:$file -xsl:dc2solr.xsl -o:$outputFile').substitute(file=file, outputFile=outputFile)		
		try:			
			os.system(cs)
			print file,"processed."			
		except:
			#this should include a logging event
			print file,"had errors and did NOT process."

	#move all files to solrXML
	os.system("mv ./setsXML/*_Solr.xml ./solrXML/")


def indexSolr():	
	#index in Solr
	fileList = funcs.listdir_fullpath('./solrXML')
	for file in fileList:			
		os.system(Template("curl -v '$baseURL/update/?commit=true' --data-binary @$file -H 'Content-type:text/xml; charset=utf-8'").substitute(file=file, baseURL=baseURL))
	


#timer
startTime = int(time.time())

#download and index
# downloadOAI()
# transformFiles()
indexSolr()

#end timer
endTime = int(time.time())
totalTime = endTime - startTime
print "Total seconds elapsed",totalTime







