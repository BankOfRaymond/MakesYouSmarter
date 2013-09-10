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
	
	def parseThesaurus(self):
		self.dbConnection.connect()
		self.dbConnection.truncateAll()
		
		f = open(self.fileName, 'rb')
		try:
			reader = csv.reader(f)
			for row in reader:
				if row[0] != '':
					# self.upsertVector(row[0],row[1:],1)  #top 
					# print
					# print row
					# print 
					for i in range(len(row)):
						if row[i] !='' or row[i] != None:
							self.dbConnection.upsertVector(row[i], row[:i]+row[i+1:] ,1)
		finally:
			f.close()
		self.dbConnection.disconnect()


	# def insertVector(self, vector, attributes, score ):
		
	# 	inDB = self.dbConnection.vectorInDB(vector)
	# 	print inDB,vector,attributes
		
	# 	# if inDB == False:
	# 	# 	self.dbConnection.insertIntoDB(vector, )








def main(args):
	#print args
	# try:
	vb = VectorBuilder(args[1])
	vb.parseThesaurus()


	# except Exception, e:
	# 	print e
	# 	print "Need to specifiy file name 'python vectorBuilder.py ../files/rgsFrame.csv'"

if __name__ == '__main__':
    sys.exit(main(sys.argv))






#open db connect
# load line by line

