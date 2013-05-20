#!/bin/bash
import sys

def analyzeSentence(sentence):
	wordArray = sentence.split(" ")
	print "Count", len(wordArray)




def main(args):
	try:		
		input = raw_input("Enter word:")
		analyzeSentence(input)
	except:
		return 1
	else:
		return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))





