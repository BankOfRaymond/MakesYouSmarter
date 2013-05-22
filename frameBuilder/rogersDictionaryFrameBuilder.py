#!/usr/bin/python
homeURL = "/home/cyrano821/MakesYouSmarter/"
import sys
import re
sys.path.append(homeURL+'frameBuilder')
sys.path.append(homeURL+'files')

# def buildFrames():
# 	#Load Files
# 	loadFiles()
# 	print "In Frame Builder"


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
			curedFrame.append(item.translate(None,",-."))

		strippedPunctuation.append(curedFrame)

	return strippedPunctuation		
	# return re.split('; | , | ',strippedPunctuation)

def main(args):
	try:	
		print "\nNAME OF FILE: ",args[1]
		openFile = parseRogersThesaurus(args[1])
	except:
		print "\nNO FILE MENTIONED"
		print "Unexpected error:", sys.exc_info()[0]
		sys.exit()

	filteredFile = filterFile(openFile)
	filteredFile = stripPunctuation(filteredFile)

	for item in filteredFile:
		.print item
		True

	#print filteredFile
	#print filteredFile[1].translate(None,';.-,')
	

if __name__ == '__main__':
    sys.exit(main(sys.argv))




