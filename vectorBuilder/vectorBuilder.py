#!/usr/bin/python
import sys
sys.path.append('/home/cyrano821/MakesYouSmarter/databaseConnections')
import csv

import databaseConnect 

''' 
	Needs to specifiy the file and directory to operate 
	Connects to database and writes to database per file
'''
class VectorBuilder():

	fileName	 	= None
	dbConnection 	= None

	def __init__(self,fileName):
		self.fileName = fileName
		self.dbConnection = databaseConnect.DatabaseConnect() 
	
	def parseFile(self):
		self.dbConnection.connect()
		f = open(self.fileName, 'rb')
		try:
			reader = csv.reader(f)
			for row in reader:
				#if len(row[0].split()) > 1:
				#print row
				print row[0], " | ", row[1:]
		finally:
			f.close()




		self.dbConnection.disconnect()






def main(args):
	print args
	# try:
	vb = VectorBuilder(args[1])
	vb.parseFile()


	# except Exception, e:
	# 	print e
	# 	print "Need to specifiy file name 'python vectorBuilder.py ../files/rgsFrame.csv'"

if __name__ == '__main__':
    sys.exit(main(sys.argv))






#open db connect
# load line by line

