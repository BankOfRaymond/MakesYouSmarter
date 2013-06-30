#!/usr/bin/python
homeURL = "/home/cyrano821/MakesYouSmarter/"
import sys
import re
import csv
import os
from string import digits
sys.path.append(homeURL+'frameBuilder')
sys.path.append(homeURL+'files')

def appendToFile(filename, contents):
	f = open(filename, 'a')
	try:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(contents)
	except Exception, e:	print False

def parseRogersThesaurus(nameOfFile):
	f = open(nameOfFile)
	lines = f.readlines()
	f.close()
	return lines

def filterFile(openFile):
	filteredLines = []
	for line in openFile:
		if "#" in line[:5] and line:
			filteredLines.append(line.rstrip())
	return filteredLines
	
def stripPunctuation(filteredFile):
	strippedPunctuation = []
	for line in filteredFile:
		temp = line
		#temp = line.translate(None,';,-.')
		a = [m.start() for m in re.finditer(r' ',temp)]	#Locates in string the blank spaces. a[0] = 0 first positino of ' ', a[1] = 5 second position of ' '
		temp = temp[a[1]:]
		frame = re.split(';|,',temp)
		
		#print frame
		curedFrame = []
		for item in frame:
		 	#if "N." not in item and "&c" not in item and  "adj." not in item and "(" not in item and item !='' and len(item)>1: # and re.match("^[A-Za-z]*$", item):
			itemToAppend = item.translate(None,",").translate(None,digits)

			#print itemToAppend

			if "&c" in itemToAppend:
				itemToAppend = itemToAppend[:itemToAppend.find("&c") - 1]
			if "c." in itemToAppend:
				itemToAppend = itemToAppend[:itemToAppend.find("&c") - 1]
			if "-- N." in itemToAppend:
				itemToAppend = itemToAppend[:itemToAppend.find("-- N.")].translate(None,".")
			if "N." in itemToAppend:
				itemToAppend = itemToAppend[:itemToAppend.find("N.") -1]
			if "[" in itemToAppend:
				itemToAppend = itemToAppend[:itemToAppend.find("[") -1] + itemToAppend[itemToAppend.find("]") +1:]

			#print itemToAppend
			curedFrame.append(itemToAppend.strip(" ").lower())
		strippedPunctuation.append(curedFrame)

	return strippedPunctuation		
	# return re.split('; | , | ',strippedPunctuation)

def main(args):
	try:	
		print "\nNAME OF FILE: ",args[1]
		openFile = parseRogersThesaurus(args[1])
	except:
		print "\nCORRECT USAGE: python rogersDictionaryFrameBuilder.py [NAME OF FILE INCLUDING DIRECTORY]"
		print "Unexpected error:", sys.exc_info()[0]
		sys.exit()

	try:	
		os.remove("/home/cyrano821/MakesYouSmarter/files/rgsFrame.csv")
		print "File successfully removed"
	except:	print "File",openFile,"Does Not Exist"

	filteredFile = filterFile(openFile)
	filteredFile = stripPunctuation(filteredFile)

	for row in filteredFile:
		#print row
		appendToFile("/home/cyrano821/MakesYouSmarter/files/rgsFrame.csv",row)
	#print filteredFile[:10]
	

	
	
	# for item in filteredFile:
	# 	print item
	# 	True

	#print filteredFile
	#print filteredFile[1].translate(None,';.-,')
	

if __name__ == '__main__':
    sys.exit(main(sys.argv))




