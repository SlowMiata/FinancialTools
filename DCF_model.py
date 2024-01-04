'''
@project       : CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Tu Ha

@Date          : 9/2023

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://github.com/JECSand/yahoofinancials


'''
import os
import pandas as pd
import numpy as np
import sqlite3
import datetime 
import math

import option
from stock import Stock

class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
        short_term_growth_rate for the next 5Y
        medium_term_growth_rate from 6Y to 10Y
        long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None


    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model
        '''
        eps5y = self.short_term_growth_rate 
        eps6to10y = self.medium_term_growth_rate
        eps10to20y = self.long_term_growth_rate 


        
        yearlyDiscountFactor = 1 / (1+ self.stock.lookup_wacc_by_beta(self.stock.get_beta()))
        freeCashFlow = self.stock.get_free_cashflow()
        CF = 0
        
        #predefining year 5 and 10 
        DCF5 = (freeCashFlow * ( 1 + eps5y)**5)
        DCF10 = DCF5 * ( 1 + eps6to10y)**(5) 
        
        for i in range(1,21):
            try:
                if i <=5:
                    #year 1-5
                    CF += (freeCashFlow * ( 1 + eps5y)**i )*  yearlyDiscountFactor ** i
            
                if 5<i <=10:
                    #year 6-10
                    CF += (DCF5 * ( 1 + eps6to10y)**(i-5)) * yearlyDiscountFactor **i
            
                if 10<i:
                    #year 11-20
                    CF += (DCF10 * ( 1 + eps10to20y)**(i-10)) * yearlyDiscountFactor **i
            except:
                raise Exception("Missing data")
                

        #calculating
        PV = self.stock.get_cash_and_cash_equivalent() - self.stock.get_total_debt() + CF
        intrinsicValue = PV/self.stock.get_num_shares_outstanding()
        return(intrinsicValue) 



def _test1():
    '''
    Tie out with the result from the medium article. The final value for APPL should be 84.88
    '''

    # override the various financial data
    class StockForTesting(Stock):
        # Mark-up Stock object for testing and tie-out purpose
        def get_total_debt(self):
            result = 112723000*1000
            return(result)

        def get_free_cashflow(self):
            result = 71706000*1000
            return(result)

        def get_num_shares_outstanding(self):
            # TODO
            # grab the number of shares number from the blog
            result = 17250000000
            # end TODO
            return(result)

        def get_cash_and_cash_equivalent(self):
            # TODO
            # grab the right number from the blog
            result = 93025000000
            # end TODO
            return(result)

        
        def get_beta(self):
            result = 1.31
            return(result)

    opt = None
    db_connection = None
    symbol = 'Testing AAPL'
    stock = StockForTesting(opt, db_connection, symbol)

    
    as_of_date = datetime.date(2020, 9, 28)
    model = DiscountedCashFlowModel(stock, as_of_date)

    print(f"Running test1 for {symbol} ")
    print("Shares ", stock.get_num_shares_outstanding())
    print("FCC ", stock.get_free_cashflow())
    beta = stock.get_beta()
    wacc = stock.lookup_wacc_by_beta(beta)
    print("Beta ", beta)
    print("WACC ", wacc)
    print("Total debt ", stock.get_total_debt())
    print("cash ", stock.get_cash_and_cash_equivalent())

    # look up EPS next 5Y from Finviz, 12.46% from the medium blog
    eps5y = 0.1246     
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print(f"DCF price for {symbol} as of {as_of_date} is {model_price}")

def _test2():
    #
    eps5YData = {'AAPL': 0.074, 'BABA': 0.1058, 'TSLA': 0.0855, 'NVDA': 0.7870, 'JNJ': 0.0575, 'MSFT':0.17870 }
    
    symbol = 'AAPL'
    #symbol = 'BABA'
    #symbol = 'NVDA'
    #symbol = 'JNJ'
    # symbol = 'TSLA'
    # symbol = 'MSFT'
    
    # default option
    opt = option.Option()
    opt.data_dir = "./data"
    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    #2023, 10, 1
    as_of_date = datetime.date(2023, 10, 1)

    stock = Stock(opt, db_connection, symbol)
    stock.load_financial_data()
    
    model = DiscountedCashFlowModel(stock, as_of_date)

    print("Shares ", stock.get_num_shares_outstanding())
    print("FCC ", stock.get_free_cashflow())
    beta = stock.get_beta()
    wacc = stock.lookup_wacc_by_beta(beta)
    print("Beta ", beta)
    print("WACC ", wacc)
    print("Total debt ", stock.get_total_debt())
    print("cash ", stock.get_cash_and_cash_equivalent())

    # look up EPS next 5Y from Finviz, 12.46% from the medium blog
    eps5y = eps5YData[symbol]

    
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)
    
    model_price = model.calc_fair_value()
    print(f"DCF price for {symbol} as of {as_of_date} is {model_price}")
    

def _test():
    _test1()
    _test2()
    
if __name__ == "__main__":
    _test()
    #_test1()
