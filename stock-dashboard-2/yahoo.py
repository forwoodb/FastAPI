import pandas as pd
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime

# connect to db
dbUrl = 'mongodb+srv://forwoodb:q84ItPYwNm77gfFO@cluster0.7vsg6zn.mongodb.net/?appName=Cluster0'
client = MongoClient(dbUrl, tls=True,  tlsAllowInvalidCertificates=True)
db = client['test']
collection = db['stocks']

for stock in collection.find():
  print(stock)