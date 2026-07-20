import pandas as pd
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime

# connect to db
dbUrl = 'mongodb+srv://forwoodb:q84ItPYwNm77gfFO@cluster0.7vsg6zn.mongodb.net/?appName=Cluster0'
client = MongoClient(dbUrl, tls=True,  tlsAllowInvalidCertificates=True)
db = client['test']
collection = db['stocks']

# Get stock data from yfinance
for stock in collection.find():
  data = yf.download(tickers=stock['ticker'], period='200d', interval='1d')

  # Reset the index to make 'Date' a regular column
  data.reset_index(inplace=True)

  # df = pd.DataFrame(data)

  # data = data.rename(columns={'Ticker': 'ticker'})
  data['ticker'] = stock['ticker']
  print(data)