'''
@project       : Temple University
@Instructor    : Dr. Alex Pang
@Date          : Sept 2023

@Student Name  : first last

https://github.com/JECSand/yahoofinancials

'''

from yahoofinancials import YahooFinancials 

class MyYahooFinancials(YahooFinancials):
    '''
    Extended class based on YahooFinancial libary

    '''
    def __init__(self, ticker, freq = 'annual'):
        YahooFinancials.__init__(self, ticker)
        self.ticker = ticker
        self.freq = freq
        self._income_statement_data = {}
        self._balance_sheet_data = {}
        self._cashflow_data = {}

    def load_latest_data(self):
        # load all the latest balance sheet, income statement and cashflow statement data
        self._get_income_statement_history()        
        self._get_balance_sheet_history()
        self._get_cashflow_statement_history()

        
    def get_income_statement_data(self, name):
        if name in self._income_statement_data.keys():
            return(self._income_statement_data[name])
        else:
            return None

    def get_balance_sheet_data(self, name):
        if name in self._balance_sheet_data.keys():
            return(self._balance_sheet_data[name])
        else:
            return None
    
    def get_cashflow_data(self, name):
        if name in self._cashflow_data.keys():
            return(self._cashflow_data[name])
        else:
            return None

        
    def print_all_data(self):
        # print all data available
        print(f"Income Statement Data as of {self._income_statement_asof_date} are")
        for k, v in self._income_statement_data.items():
            print(f"{k}: {v}")
        print("\n\n")
        print(f"Balance Sheet Data as of {self._balance_sheet_asof_date} are")
        for k, v in self._balance_sheet_data.items():
            print(f"{k}: {v}")
        print("\n\n")
        print(f"Cashflow Statement Data as of {self._cashflow_asof_date} are")
        # show all data available
        for k, v in self._cashflow_data.items():
            print(f"{k}: {v}")
            
    def _get_income_statement_history(self):
        if self.freq == 'annual':
            key = 'incomeStatementHistory'
        elif self.freq == 'quarterly':
            key = 'incomeStatementHistoryQuarterly'

        # save the latest history
        hist = self.get_financial_stmts(self.freq, 'income')[key][self.ticker][-1]
        dt = list(hist.keys())[0]
        self._income_statement_asof_date = dt
        # cashflow data is a dict
        self._income_statement_data = hist[dt]
        
    def _get_balance_sheet_history(self):
        if self.freq == 'annual':
            key = 'balanceSheetHistory'
        elif self.freq == 'quarterly':
            key = 'balanceSheetHistoryQuarterly'

        # save the latest history
        hist = self.get_financial_stmts(self.freq, 'balance')[key][self.ticker][-1]
        dt = list(hist.keys())[0]
        self._balance_sheet_asof_date = dt
        # cashflow data is a dict
        self._balance_sheet_data = hist[dt]
        
    def _get_cashflow_statement_history(self):
        #
        if self.freq == 'annual':
            key = 'cashflowStatementHistory'
        elif self.freq == 'quarterly':
            key = 'cashflowStatementHistoryQuarterly'

        # save the latest history
        hist = self.get_financial_stmts(self.freq, 'cash')[key][self.ticker][-1]
        dt = list(hist.keys())[0]
        self._cashflow_asof_date = dt
        # cashflow data is a dict
        self._cashflow_data = hist[dt]
            
def _test():
    symbol = 'AAPL'
    freq='quarterly'
    
    yfinance = MyYahooFinancials(symbol, freq)

    yfinance.load_latest_data()
    
    print(f"Getting Financial Data for {symbol} with freq {freq}\n\n")
    
    yfinance.print_all_data()
    # example of how to get some of the data
    print("Total Revenue: ", yfinance.get_income_statement_data('totalRevenue'))    
    print("Free Cashflow: ", yfinance.get_cashflow_data('freeCashFlow'))


if __name__ == "__main__":
    _test()
