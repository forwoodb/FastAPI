import pandas as pd
import yfinance as yf
from pymongo import MongoClient
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()
@app.get('/get_stocks')
def get_stocks():
  # connect to db
  dbUrl = 'mongodb+srv://forwoodb:q84ItPYwNm77gfFO@cluster0.7vsg6zn.mongodb.net/?appName=Cluster0'
  client = MongoClient(dbUrl, tls=True,  tlsAllowInvalidCertificates=True)
  db = client['test']
  collection = db['stocks']

  # create dataframe
  df = pd.DataFrame()

  # Get stock data from yfinance
  for stock in collection.find():
    data = yf.download(tickers=stock['ticker'], period='200d', interval='1d')

    # Reset the index to make 'Date' a regular column
    data.reset_index(inplace=True)

    data = data.round(2)

    # add 'ticker' column
    data['ticker'] = stock['ticker']

    # drop 2nd level of column headers
    data.columns = data.columns.droplevel(1)

    # add timestamp column
    data['Time'] = datetime.now().strftime('%H:%M:%S')

    # add moving average columns
    data['200D'] = data['Close'].rolling(200).mean().round(2)
    data['100D'] = data['Close'].rolling(100).mean().round(2)
    data['50D'] = data['Close'].rolling(50).mean().round(2)
    data['20D'] = data['Close'].rolling(20).mean().round(2)
    data['10D'] = data['Close'].rolling(10).mean().round(2)
    data['5D'] = data['Close'].rolling(5).mean().round(2)

    # drop every row except the last 
    data = data.tail(1)

    df = pd.concat((df, data), ignore_index=True)

    # df = pd.DataFrame(data)

    # data = data.rename(columns={'Ticker': 'ticker'})
    

  json_out = df.to_dict(orient='records')
  print(json_out)
  return json_out