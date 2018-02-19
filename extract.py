#!/usr/bin/python2.7

import requests
import os, sys
import argparse
import validators
import xmltodict
import string

parser = argparse.ArgumentParser(description='This script is meant for the extraction of wiki content from the "Humansiten Wiki".')
parser.add_argument('-p', '--pagename', dest='PAGENAME', default='Leitbild', action='store', type=str, help='Name of the wiki page to be extracted') # might use nargs='+' too

args = parser.parse_args()

def geturl(givenName):
	if validators.url(givenName):
		url, page = string.rsplit(givenName, '/', maxsplit=1)
		pagename = url + '/Spezial:Exportieren/' + page
	else:
		pagename = 'https://wiki.diehumanisten.de/wiki/index.php/Spezial:Exportieren/' + givenName
	if not validators.url(pagename):
		raise Exception("This is not a valid url: " + pagename )
	return pagename

def getxmldict(url):
	xml_request = requests.get(url)
	if not xml_request.status_code == 200:
		raise Exception("Bad status code" + str(xml_request.status_code) )
	xml = xmltodict.parse(xml_request.text)
	return xml

def getContent(xmlDict):
	return xmlDict['mediawiki']['page']['revision']['text']['#text']

url = geturl(args.PAGENAME)
xmlDict = getxmldict(url)
content = getContent(xmlDict)
print content
