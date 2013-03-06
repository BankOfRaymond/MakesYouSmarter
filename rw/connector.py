#!/usr/bin/python
# connector.py


import pymongo
import cgitb
print "Content-Type: text/html\n\n"

connection = pymongo.Connection('localhost', 27017)
db = connection.test

collection = db.test
print db