
import pymongo


connection = pymongo.Connection('localhost', 27017)
db = connection.test

collection = db.test
print collection