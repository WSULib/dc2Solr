# Utility designed to pull records from Digital Commons, via OAI, and index them in Solr
import os
import sys
import xml.etree.ElementTree as ET
import urllib, urllib2
from string import Template
import time
#workhorse functions found in funcs.py
import funcs

'''
Takes arguments: 'all' OR combination of 'download', 'transform', and 'index'
Will run each function, in proper order, if argument present when running script.
'''

#which functions to run
funcArgs = sys.argv

#global vars
baseURL = "http://localhost/solr4/DCOAI"
baseOAI = "http://digitalcommons.wayne.edu/do/oai/?"
saxonLocation = "/var/opt/fedora_utilities/saxon9he.jar"

#timer
startTime = int(time.time())

#check script parameters, begin download, transform, index
if "all" in funcArgs:
	funcs.downloadOAI(baseOAI)
	funcs.transformFiles(saxonLocation)
	funcs.indexSolr(baseURL)
else:
	if "download" in funcArgs:
		funcs.downloadOAI(baseOAI)
	if "transform" in funcArgs:
		funcs.transformFiles(saxonLocation)
	if "index" in funcArgs:
		funcs.indexSolr(baseURL)
if len(funcArgs) == 1:
	print "No functions called, nothing to do. Try combination of 'download', 'transform', and 'index' as arguments, or 'all' to run all tasks."

#end timer
endTime = int(time.time())
totalTime = endTime - startTime
print "Total seconds elapsed",totalTime







