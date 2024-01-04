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
import math
import datetime 
import sqlite3

from utils import MyYahooFinancials 
import option

class Stock(object):
    '''
    Stock class for getting financial statements
    default freq is annual
    '''
    def __init__(self, opt, db_connection, ticker, spot_price = None, sigma = None, dividend_yield = 0, freq = 'annual'):
        self.opt = opt
        self.db_connection = db_connection
        self.ticker = ticker
        self.spot_price = spot_price
        self.sigma = sigma
        self.dividend_yield = dividend_yield
        
        self.yfin = MyYahooFinancials(ticker, freq)

    def get_daily_hist_price(self, start_date, end_date):
        # Get daily historical OHLCV from database
        try:
            sql = f"select * from EquityDailyPrice where ticker = '{self.ticker}' order by AsOfDate asc"
            df = pd.read_sql(sql, self.db_connection)
            df['AsOfDate'] = df['AsOfDate'].apply(lambda x: datetime.datetime.strptime(x[:10], "%Y-%m-%d").date())

            # filter data between start and end date
            df = df[ df.AsOfDate >= start_date ]
            df = df[ df.AsOfDate <= end_date ]

            # create an index based on the AsOfDate column
            df['Date'] = df.AsOfDate
            df = df.set_index('Date')
            
            self.ohlcv_df = df
            return(df)
            
        except Exception as e:
            print(f"Failed to get data for {self.ticker}: {e}")
            raise Exception(e)

    def load_financial_data(self):
        #
        print(f"Loading financial data for {self.ticker}")
        self.yfin.load_latest_data()
        
    def calc_returns(self):
        # ...
        self.ohlcv_df['prev_Close'] = self.ohlcv_df['Close'].shift(1)
        self.ohlcv_df['returns'] = (self.ohlcv_df['Close'] - self.ohlcv_df['prev_Close'])/ \
                                        self.ohlcv_df['prev_Close']
        
    def get_total_debt(self):
    
        result = self.yfin.get_balance_sheet_data('totalDebt')
        return(result)

    def get_free_cashflow(self):
    
        result = self.yfin.get_cashflow_data('freeCashFlow')
        return(result)

    def get_cash_and_cash_equivalent(self):
    
        result = self.yfin.get_balance_sheet_data('cashCashEquivalentsAndShortTermInvestments')
        return(result)

    def get_num_shares_outstanding(self):

        result = self.yfin.get_num_shares_outstanding()
        
        return(result)

    def get_beta(self):
    
        result =self.yfin.get_beta()
        return(result)

    def lookup_wacc_by_beta(self, beta):
        if beta == None:
            print("no beta found")
            return -1
        
        if(beta < .8):
            result = .05
        elif (.8 <= beta < 1):
            result = .06
        elif (1 <= beta < 1.1):
            result = .065
        elif (1.1 <= beta < 1.2):
            result = .07
        elif (1.2 <= beta < 1.3):
            result = .075
        elif (1.3 <= beta < 1.5):
            result = .08
        elif (1.5 <= beta < 1.6):
            result = .085
        elif (beta > 1.6):
            result = .09
        
        return(result)
        

def _test():
    # a few basic unit tests
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)

    print(vars(opt))
    
    symbol = 'AAPL'
    freq = 'quarterly'
    stock = Stock(opt, db_connection, symbol, freq = freq)

    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2023, 10, 1)
    df = stock.get_daily_hist_price(start_date, end_date)
    print(df.head())

    stock.load_financial_data()
    print(f"Getting Financial Data for {symbol} with freq {freq}")

    beta = stock.get_beta()

    print('Total Debt: ', stock.get_total_debt())
    print('Free Cashflow: ', stock.get_free_cashflow())
    print('Cash and Cash equivalent: ', stock.get_cash_and_cash_equivalent())
    print('Shares outstanding: ', stock.get_num_shares_outstanding())
    print(beta)
    print('WACC: ', stock.lookup_wacc_by_beta(beta))
    
if __name__ == "__main__":
    _test()
