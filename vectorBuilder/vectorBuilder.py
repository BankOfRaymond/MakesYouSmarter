#!/usr/bin/python
import sys
sys.path.append('/home/cyrano821/MakesYouSmarter/databaseConnections')


import databaseConnect 



def main(args):
	print args
	db = databaseConnect.connectToDB()

	databaseConnect.disconnectFromDB(db)

if __name__ == '__main__':
    sys.exit(main(sys.argv))






#open db connect
# load line by line

