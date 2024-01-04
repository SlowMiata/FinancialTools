'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Tu Ha

@Date          : 9/1/2023

Download daily stock price from Yahoo

'''


import os
import pandas as pd
import numpy as np
import sqlite3

# pip install pandas-datareader
import pandas_datareader as pdr

import yfinance as yf

import option

# https://www.geeksforgeeks.org/python-stock-data-visualisation/

class Fetcher(object):

    def __init__(self, opt, db_connection):
        # opt is an option instance
        self.opt = opt
        self.db_connection = db_connection

    def get_daily_from_yahoo(self, ticker, start_date, end_date):
        
        stock = yf.Ticker(ticker)
        
        #save the daily stock data into data frame df
        df = stock.history(start=start_date,end=end_date)
        
        #check if there is data for the ticker
        if df.shape[0] == 0:
            print("no data for {}".format(ticker))
        return(df)
    

    def download_data_to_csv(self, list_of_tickers):
        
        for ticker in list_of_tickers:
            
            # get the daily data
            df = self.get_daily_from_yahoo(ticker,self.opt.start_date,self.opt.end_date)
            
            #create a new column in the data frame for Ticker
            df['Ticker'] = ticker
            ##create a new file for each ticker 
            file = os.path.join(self.opt.output_dir, f"{ticker}_daily.csv")
            
            #turn the data frame into a csv file
            df.to_csv(file,sep=',')
    
    
        
    def csv_to_table(self, csv_file_name, fields_map, db_table):
        # insert data from a csv file to a table
        
        # use self.db_connection
        # insert data from a csv file to a table
        df = pd.read_csv(csv_file_name)
        if df.shape[0] <= 0:
            return
        # change the column header
        df.columns = [fields_map[x] for x in df.columns]

        # move ticker columns
        new_df = df[['Ticker']]
        for c in df.columns[:-1]:
            new_df[c] = df[c]

        ticker = os.path.basename(csv_file_name).replace('.csv','').replace("_daily", "")
        print(ticker)
        cursor = self.db_connection.cursor()

        
        #delete any old data from the ticker
        delete_sql = f"DELETE FROM {db_table} WHERE Ticker = '{ticker}'"
        cursor.execute(delete_sql)
        #create a large tuple for all the data in the data frame
        db_tuple = [tuple(x) for x in new_df.values]
        
        #insert each row into the database
        sql = f"INSERT INTO {db_table} (Ticker, AsOfDate, Open, High, Low, Close, Volume, Dividend, StockSplit) VALUES (?,?,?,?,?,?,?,?,?)"
        print(sql)
        cursor.executemany(sql,db_tuple)
        
        self.db_connection.commit()
        cursor.close()

        
        return
        
    def save_daily_data_to_sqlite(self, daily_file_dir, list_of_tickers):
        # read all daily.csv files from a dir and load them into sqlite table
        db_table = 'EquityDailyPrice'

        fields_map = {'Date': 'AsOfDate', 'Dividends': 'Dividend', 'Stock Splits': 'StockSplits'}
        for f in ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']:
            fields_map[f] = f

        
        #  for ticker in list_of_tickers:
        for ticker in list_of_tickers:
            file_name = os.path.join(daily_file_dir, f"{ticker}_daily.csv")
            print(file_name)
            self.csv_to_table(file_name, fields_map,db_table)

    

    
def run():
    #
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")
    
    if opt.tickers is not None:
        list_of_tickers = opt.tickers.split(',')
    else:
        fname = os.path.join(opt.data_dir, "S&P500.txt")
        list_of_tickers = list(pd.read_csv(fname, header=None).iloc[:, 0])
        print(f"Read tickers from {fname}")
        

    print(list_of_tickers)
    print(opt.start_date, opt.end_date)

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    
    fetcher = Fetcher(opt, db_connection)
    print(f"Download data to {opt.data_dir} directory")

    # Call the fetcher download and save_daily methods

    
    fetcher.download_data_to_csv(list_of_tickers)
    fetcher.save_daily_data_to_sqlite(opt.output_dir, list_of_tickers)


    
    
    #Test the get daily from yahoo
def _test():
    a = 0
    b = 0
    ticker = 'MSFT'
    start_date = '2020-01-01'
    end_date = '2023-08-01'

    print (f"Testing getting data for {ticker}:")
    fetcher = Fetcher(a,b)
    
    
    df = fetcher.get_daily_from_yahoo(ticker, start_date, end_date)
    print(df)
    
if __name__ == "__main__":
    #_test()
    run()
