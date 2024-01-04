'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Tu Ha

@Date          : 11/2023

Black-Schole Model

'''

import datetime
from scipy.stats import norm
from math import log, exp, sqrt

from stock import Stock
from financial_option import *

class BlackScholesModel(object):
    '''
    Implementation of the Black-Schole Model for pricing European options
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None 
        if option.option_type == FinancialOption.Type.CALL:
            
            #gives the price of the the put based on the call
            result = option_price + option.strike * exp(-self.risk_free_rate * option.time_to_expiry) - option.underlying.spot_price
            
        elif option.option_type == FinancialOption.Type.PUT:
            
            #gives the price of the call based on the put
            result = option_price + option.underlying.spot_price - option.strike * exp(-self.risk_free_rate * option.time_to_expiry)
            
        return(result)

    def calc_model_price(self, option):
        '''
        Calculate the price of the option using Black-Scholes model
        '''
        px = None
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        else:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate
            
            d1 = (log(S0/K)+(r-q+pow(sigma, 2)/2)*T)/(sigma * sqrt(T))
            d2 = (d1 - (sigma * sqrt(T)))
            
            if option.option_type == FinancialOption.Type.CALL:
                
                px = S0 * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

                
            elif option.option_type == FinancialOption.Type.PUT:
                px = K * exp(-r * T) * norm.cdf(-d2) - S0 * exp(-q * T) * norm.cdf(-d1)
            
            
        return(px)

    def calc_delta(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            
            d1 = (log(S_0/K)+(r-q+pow(sigma, 2)/2)*T)/(sigma * sqrt(T))
            
            if option.option_type == FinancialOption.Type.CALL:
                result = exp(-q * T) * norm.cdf(d1)
                
            elif option.option_type == FinancialOption.Type.PUT:
                result = exp(-q * T) * (norm.cdf(d1) - 1)
            
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_gamma(self, option):

        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            
            d1 = (log(S_0/K)+(r-q+pow(sigma, 2)/2)*T)/(sigma * sqrt(T))
            
        
            result = exp(-q * T) * norm.pdf(d1) / (S_0 * sigma * sqrt(T))
                
        else:
            raise Exception("Unsupported option type")
        return result

    def calc_theta(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            if option.option_type == FinancialOption.Type.CALL:
                result = (-S_0 * norm.pdf(d1) * sigma * exp(-q * T)) / (2 * sqrt(T)) + \
                         (q * S_0 * norm.cdf(d1) * exp(-q * T)) - (r * K * exp(-r * T) * norm.cdf(d2))
            else:
                result = (norm.pdf(d1) * exp(-q * T)) / (S_0 * sigma * sqrt(T)) - \
                         (q * S_0 * norm.cdf(-d1) * exp(-q * T)) + (r * K * exp(-r * T) * norm.cdf(-d2))
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_vega(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))

            
            result = S_0 * sqrt(T) * norm.pdf(d1) * exp(-q * T)
        else:
            raise Exception("Unsupported option type")

        return result

    def calc_rho(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            sigma = option.underlying.sigma
            q = option.underlying.dividend_yield
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            
            if option.option_type == FinancialOption.Type.CALL:
                result = K * T * exp(-r * T) * norm.cdf(d2)
            
            elif option.option_type == FinancialOption.Type.PUT:
                result = -K * T * exp(-r * T) * norm.cdf(-d2)
            
        else:
            raise Exception("Unsupported option type")
        return result


def _test():
    pass

if __name__ == "__main__":
    _test()
