#!/usr/bin/python

homeURL = "/home/cyrano821/MakesYouSmarter/"

import sys
sys.path.append(homeURL+'databaseConnections')
sys.path.append(homeURL+'frameBuilder')
sys.path.append(homeURL+'files')
from databaseConnect import *
from frameBuilder import *

def analyzeSentence(sentence):
	wordArray = sentence.split(" ")
	print "Count", len(wordArray)

def main(args):
	# try:
	connectToDB()
	print "\n"
	print "1: Build Frame Files"
	print "2: Build Vector Files"
	print "3: Analyze Sentence"
	input = raw_input("\nWhat do you want to do:")

	if   input == "1":	buildFrames()
	elif input == "2":	print "Build Vector Files"
	elif input == "3":	print "Analyze Sentence"
	else:	print "Unknown Input"



	disconnectFromDB()
	# except:
	# 	return 1
	# else:
	# 	return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))





