#!/usr/bin

import MySQLdb
import credentials

class DatabaseConnect():
	USERNAME = None
	PASSWORD = None
	HOST 	 = None
	DATABASE = None

	dbConnection = None

	def __init__(self):
		self.USERNAME 	= credentials.USERNAME
		self.PASSWORD	= credentials.PASSWORD
		self.HOST		= credentials.HOST
		self.DATABASE 	= credentials.DATABASE

	def connect(self):
		self.dbConnection = MySQLdb.connect(self.HOST, self.USERNAME, self.PASSWORD, self.DATABASE)

	def disconnect(self):
		self.dbConnection.close()

	def vectorInDB(self,vector):
		cursor = self.dbConnection.cursor()
		query = "".join(("SELECT vector_id from ", self.DATABASE,".",'vector WHERE vector ="',vector,'"'))
		cursor.execute(query)
		r = cursor.fetchall()
		if (len(r) <1):
			return False
		else:
			return r[0]

	def upsertVector(self,vector,attributes, score):
		cursor = self.dbConnection.cursor()
		inDB = self.vectorInDB(vector)

		if inDB == False:
			query = "".join(("INSERT INTO ",self.DATABASE, '.vector (vector) VALUES ("', vector  ,'")' ))
			cursor.execute(query)
			vector_id = self.dbConnection.insert_id()
			for attrib in attributes:
				if attrib != '' and attrib != None:
					query = "".join(( "INSERT INTO ",self.DATABASE, '.' ,'attribute (vector_id, attribute,score) VALUES (',\
						str(int(vector_id)), ',"',attrib,'",', str(score),')'     ))
					cursor.execute(query)
		elif inDB:
			for attrib in attributes:
				if attrib != '' and attrib != None:
					query = "".join(( "SELECT * FROM ",self.DATABASE,".attribute WHERE vector_id=",str(inDB[0]),' AND attribute="',attrib, '" '  ))
					cursor.execute(query)
					itemExists = cursor.fetchall()
					if itemExists == None or itemExists == ():
						query = "".join(( "INSERT INTO ",self.DATABASE, '.' ,'attribute (vector_id, attribute,score) VALUES (',\
							str(inDB[0]), ',"',attrib,'",', str(score),')'     ))
					cursor.execute(query)
		self.dbConnection.commit()

	def truncateAll(self):
		cursor = self.dbConnection.cursor()
		query = "TRUNCATE TABLE vector"
		cursor.execute(query)
		query = "TRUNCATE TABLE attribute"
		cursor.execute(query)
		self.dbConnection.commit()



			


	# def isInDB(self,table, inColumn, outColumn, data):
	# 	cursor = self.dbConnection.cursor()
	# 	query = "".join(("SELECT ",outColumn," from ", self.DATABASE,".",table, " WHERE ", inColumn, " = '",str(data),"'"))
	# 	cursor.execute(query)
	# 	r = cursor.fetchall()
	# 	if(len(r) < 1):
	# 		return False
		# else:
		# 	return r[0]

	# def insert(self,table,columns,data):
	# 	query = "INSERT INTO " + self.DATABASE+"."+table + " ( " + ",".join(columns) + " ) " + " VALUES " + "(" +str(data)[1:-1] + ")"
	# 	cursor = self.dbConnection.cursor()
	# 	cursor.execute(query)
	# 	self.dbConnection.commit()

	# def truncate(self, table):
	# 	cursor = self.dbConnection.cursor()
	# 	query = "".join(("TRUNCATE TABLE ",self.DATABASE,".",table))
	# 	self.dbConnection.commit()

	# def showAll(self):
	# 	query = "SELECT * from listing;"
	# 	cursor = self.dbConnection.cursor()
	# 	cursor.execute(query)
	# 	print cursor.fetchall()


	# 	query = "SELECT * from category;"
	# 	cursor = self.dbConnection.cursor()
	# 	cursor.execute(query)
	# 	print cursor.fetchall()




# d = DBControl()
# d.connect()
# print d.isInDB("listing","ebay_item_id ", "ebay_item_id","1")
# d.disconnect()



'''
def checkSymbolInDB(stock_symbol):
	#database = connectToDB()
	cursor = database.cursor()
	cursor.execute("SELECT count(*) from Finance.symbol WHERE symbol = %s", (stock_symbol.upper()) )
	isInDB = False
	if cursor.fetchone()[0] > 0:	isInDB = True
	#disconnectFromDB(database)
	return isInDB

def getCompanyName(stock_symbol):
	#database = connectToDB()
	cursor = database.cursor()
	cursor.execute("SELECT name from Finance.symbol WHERE symbol=%s", (stock_symbol.upper()))
	try:	company_name = cursor.fetchone()[0]
	except:	company_name = ""
	#disconnectFromDB(database)
	return company_name

#exchange is str takes in Exchange name. ListofStocks - structure [[str:Symbol, str:"Name Of company"]]
def insertListOfSymbols(exchange, listOfStocks):
	#database = connectToDB()
	cursor = database.cursor()
	for stock in listOfStocks:
		cursor.execute("SELECT count(*) from Finance.symbol WHERE symbol=%s AND exchange=%s", (stock[0],exchange))
		if cursor.fetchone()[0] == 0:
			cursor.execute("INSERT INTO Finance.symbol (symbol,name,exchange) VALUES (%s,%s,%s)",(stock[0], stock[1], exchange))
		else:
			cursor.execute("UPDATE Finance.symbol SET name=%s, exchange=%s WHERE symbol=%s AND exchange=%s",(stock[1],exchange,stock[0],exchange))
		database.commit()
		print stock[0] + "Inserted Into DB"
	#disconnectFromDB(database)

def getListOfSymbols(exchange):	#passing "ALL" gives you all stocks.
	#database = connectToDB()
	cursor = database.cursor()
	if exchange == "ALL":
		try:	cursor.execute("SELECT symbol FROM Finance.symbol")
		except MySQLdb.Error, e:	print "Error %d: %s" % (e.args[0], e.args[1])
	else:
		try:	cursor.execute("SELECT symbol FROM Finance.symbol WHERE exchange=%s", (exchange))
		except MySQLdb.Error, e:	print "Error %d: %s" % (e.args[0], e.args[1]) 
	#disconnectFromDB(database)
	return [row[0] for row in cursor.fetchall()]

# Flush out Finance.symbol
def flushOutdatedSymbols():
	stockListDirectory = "/home/bitnami/QuantMatch/crawlers/stockSymbolList/"
	exchanges = ['OTCBB', 'AMEX', 'NASDAQ', 'NYSE']
	currentStocks = []
	for exchange in exchanges:
		f = open(stockListDirectory + exchange + '.csv')
		stocks = f.readlines()
		for stock in stocks:
			currentStocks.append(stock.split(' | ')[0])
	databaseStocks = getListOfSymbols('ALL')
	for databaseStock in databaseStocks:
		if databaseStock not in currentStocks:
			query = "DELETE FROM Finance.symbol WHERE symbol='%s';" % (databaseStock)
			cursor = database.cursor()
			cursor.execute(query)
			database.commit()
			print databaseStock + " Deleted"

def getStockID(symbol):  #Needs to differentiate from exchanges
	#database = connectToDB()
	cursor = database.cursor()
	query = "SELECT symbol_id FROM Finance.symbol WHERE symbol='%s'" % (symbol)
	try:	cursor.execute(query)
	except:	True
	#disconnectFromDB(database)
	try:
		return cursor.fetchone()[0]
	except TypeError:
		return False

def getSymbol(symbol_id):  #Needs to differentiate from exchanges
	#database = connectToDB()
	cursor = database.cursor()
	try:	cursor.execute("SELECT symbol FROM Finance.symbol WHERE symbol_id=%s ", (symbol_id))
	except:	
		#disconnectFromDB(database)
		return False
	#disconnectFromDB(database)
	return cursor.fetchone()[0]

def writeToLog(problem):
	#database = connectToDB()
	cursor = database.cursor()
	try:	
		cursor.execute("INSERT INTO Finance.logError (description) VALUES (%s)", (problem))
		database.commit()
	except:	print "FAIL"
	#disconnectFromDB(database)

# returns a tuple: element 0 -> list with all the prices, element 1: date corresponding to the last element of the list of prices
def getStockEOD(symbol, interval, trade_date):
	#database = connectToDB()
	cursor = database.cursor()
	symbol_id = getStockID(symbol)
	if symbol_id:
		query = "SELECT * FROM stock_price WHERE trade_date > DATE_SUB('" + trade_date + "', INTERVAL " + str(interval) + " DAY) AND trade_date <= '" + trade_date + "' AND symbol_id = '" + str(symbol_id) + "' ORDER BY trade_date ASC;"
		cursor.execute(query)
		results = list(cursor.fetchall())
		EODPrices = []
		for result in results:
			EODPrices.append(result[6])
		#disconnectFromDB(database)
		return EODPrices
	else:
		return []

def getStockEODFromStartDate(symbol, interval, trade_date):
	#database = connectToDB()
	cursor = database.cursor()
	symbol_id = getStockID(symbol)
	if symbol_id:
		query = "SELECT * FROM stock_price WHERE trade_date < DATE_ADD('" + trade_date + "', INTERVAL " + str(interval) + " DAY) AND trade_date >= DATE_SUB('" + trade_date + "', INTERVAL 1 DAY) AND symbol_id = '" + str(symbol_id) + "' ORDER BY trade_date ASC;"
		cursor.execute(query)
		results = list(cursor.fetchall())
		EODPrices = []
		for result in results:
			EODPrices.append(result[6])
		#disconnectFromDB(database)
		return EODPrices
	else:
		return []

def insertStockPriceIntoDB(symbol_id, stockInfo):		
	#database = connectToDB()
	cursor = database.cursor()
	symbol			= getSymbol(symbol_id)
	symbol_id		= symbol_id
	trade_date 		= stockInfo[0]
	open_price 		= stockInfo[1]
	high_price		= stockInfo[2]
	low_price		= stockInfo[3]
	close_price		= stockInfo[4]
	volume 			= stockInfo[5]
	adj_close		= stockInfo[6]
	SP500 	= "%5EGSPC"

	beta = calculateBeta(getStockEOD(symbol, 90, trade_date), getStockEOD(SP500, 90, trade_date))
	query = "SELECT count(*) FROM Finance.stock_price WHERE symbol_id='%s' AND trade_date='%s'" % (symbol_id, trade_date)
	cursor.execute(query)
	results = cursor.fetchone()[0]

	if results == 0:
		query = "INSERT INTO Finance.stock_price (symbol_id, trade_date, open_price, high_price, low_price, close_price, volume, adj_close, beta) \
		VALUES ('%s','%s','%s','%s','%s','%s','%s','%s', '%s')" \
		% (symbol_id, trade_date, open_price, high_price, low_price, close_price, volume, adj_close, beta)
	else:
		query = ("Update Finance.stock_price SET open_price=%s, high_price=%s, low_price=%s, close_price=%s, volume=%s, adj_close=%s, beta=%s  \
		WHERE symbol_id='%s' AND trade_date='%s' Limit 1") \
		% (open_price, high_price, low_price, close_price, volume, adj_close, beta, symbol_id, trade_date)
	cursor.execute(query)
	database.commit()
	#disconnectFromDB(database)

def getSymbolData(symbol, date):
	#database = connectToDB()
	cursor = database.cursor()
	symbol_id = getStockID(symbol)
	query = "SELECT * FROM stock_price WHERE trade_date > DATE_SUB('" + date + "', INTERVAL 7 DAY) AND trade_date <= '" + date + "' AND symbol_id = '" + str(symbol_id) + "' ORDER BY trade_date ASC;"
	cursor.execute(query)
	results = list(cursor.fetchall())
	database.commit()
	#disconnectFromDB(database)
	return results[len(results) - 1]

def updateBeta(symbol, interval, trade_date):
	symbol_id = getStockID(symbol)
	stockData = getStockEOD('AAPL', interval, trade_date)
	SPData = getStockEOD('%5EGSPC', interval, trade_date)
	beta = calculateBeta(stockData, SPData)
	#database = connectToDB()
	cursor = database.cursor()
	query = "UPDATE Finance.stock_price SET beta='" + str(beta) + "' WHERE symbol_id = '" + str(symbol_id) + "' AND trade_date = '" + trade_date + "';"
	cursor.execute(query)
	database.commit()
	#disconnectFromDB(database)

def updateRealTimeData(cursor, stockData):
	query = "SELECT COUNT(*) FROM `Finance`.`real_time_stock_data` WHERE symbol = '" + stockData[0] + "'"
	cursor = database.cursor()
	cursor.execute(query)
	result = cursor.fetchone()[0]
	if result == 0:
		query = "INSERT INTO `Finance`.`real_time_stock_data` (symbol, last_trade_time, current_price, change_in_price, percentage_change, open_price, day_high, day_low, volume, average_daily_volume) \
		VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
		% (stockData[0], stockData[1], stockData[2], stockData[3], stockData[4], stockData[5], stockData[6], stockData[7], stockData[8], stockData[9])
	else:
		query = "UPDATE `Finance`.`real_time_stock_data` SET last_trade_time='%s', current_price='%s', change_in_price='%s', percentage_change='%s', open_price='%s', day_high='%s', day_low='%s', volume='%s', average_daily_volume='%s' \
		WHERE symbol='%s'" % (stockData[1], stockData[2], stockData[3], stockData[4], stockData[5], stockData[6], stockData[7], stockData[8], stockData[9], stockData[0])
	cursor.execute(query)
	database.commit()
	print stockData[0] + " Updated"

#bm for benchmark
def getSymbolData(symbol):
	symbol_id = getStockID(symbol)
	query = "SELECT `trade_date`, `close_price` FROM `Finance`.`stock_price` where `symbol_id` = '" + str(symbol_id) + "' ORDER BY `trade_date` DESC";
	cursor = database.cursor()
	cursor.execute(query)
	return list(cursor.fetchall())


# input outlier into anomalies
def inputOutliers(date, ret, id):
	cursor = database.cursor()
	query = "INSERT INTO `Finance`.`anomalies` (`anomaly_date`, `anomaly_return`, `symbol_id`) VALUES ('" + str(date) + "', '" + str(ret) + "', '" + str(id) + "')"
	cursor.execute(query)
	database.commit()

# remove stock
def removeStock(symbol):
	symbol_id = getStockID(symbol)
	cursor = database.cursor()
	query = "DELETE FROM `Finance`.`symbol` WHERE `symbol_id` = '" + str(symbol_id) + "'"
	cursor.execute(query)
	database.commit()

	cursor = database.cursor()
	query = "DELETE FROM `Finance`.`stock_price` WHERE `symbol_id` = '" + str(symbol_id) + "'"
	cursor.execute(query)
	database.commit()


'''