'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : first last

@Date          : 11/2023

A Simple Option Class

'''
import enum
import calendar
import math
import pandas as pd
import numpy as np


class FinancialOption(object):
    '''
    time_to_expiry is the number of days till expiry_date expressed in unit of years
    underlying is the underlying stock object
    '''

    class Type(enum.Enum):
        CALL = "Call"
        PUT  = "Put"

    class Style(enum.Enum):
        EUROPEAN = "European"
        AMERICAN = "American"

    def __init__(self, option_type, option_style,  underlying, time_to_expiry, strike):
        self.option_type = option_type
        self.option_style = option_style
        self.underlying = underlying
        self.time_to_expiry = time_to_expiry
        self.strike = strike

class EuropeanCallOption(FinancialOption):
    def __init__(self, underlying, time_to_expiry, strike):
        FinancialOption.__init__(self, FinancialOption.Type.CALL, FinancialOption.Style.EUROPEAN,
                        underlying, time_to_expiry, strike)

class EuropeanPutOption(FinancialOption):
    def __init__(self, underlying, time_to_expiry, strike):
        FinancialOption.__init__(self, FinancialOption.Type.PUT, FinancialOption.Style.EUROPEAN,
                        underlying, time_to_expiry, strike)

class AmericanCallOption(FinancialOption):
    def __init__(self, underlying, time_to_expiry, strike):
        FinancialOption.__init__(self, FinancialOption.Type.CALL, FinancialOption.Style.AMERICAN,
                        underlying, time_to_expiry, strike)

class AmericanPutOption(FinancialOption):
    def __init__(self, underlying, time_to_expiry, strike):
        FinancialOption.__init__(self, FinancialOption.Type.PUT, FinancialOption.Style.AMERICAN,
                        underlying, time_to_expiry, strike)


