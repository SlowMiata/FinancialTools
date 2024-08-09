'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : first last

@Date          : Fall 2023

A Simple Mortgage Calculator
'''

import sys
import math
from bisection_method import bisection

class MortgageCalculator(object):

    def __init__(self, loan_amount, int_rate, term):
        self.loan_amount = loan_amount
        self.int_rate = int_rate
        self.term = term
        
    def _calc_next_month_balance(self, prev_balance, level_payment, int_rate):
        # return next month balance on given previous month balance, level payment and interest rate
        principal_payment = level_payment - prev_balance * int_rate/12
        return (prev_balance - principal_payment)
        
    def _last_month_balance(self, level_payment):
        # calculate the last month balance
        prev_bal = self.loan_amount
        for i in range(12 * self.term):
            next_bal = self._calc_next_month_balance(prev_bal, level_payment, self.int_rate)
            prev_bal = next_bal
        return(prev_bal)

    def calc_level_payment(self):
        # calculate the level payment of a mortgage by requiring the last balance to be zero.
        # solve the equation using Bi-section method.
        a = self.loan_amount * (1 + self.int_rate * self.term)/(12* self.term)
        b = a/2
    
        solution, no_iterations = bisection(self._last_month_balance, a, b, eps=1.0e-6)
        return(solution)

    def compute_level_payment_analytically(self):
        # use the analytical formula to compute the level payment
        n = self.term * 12
        monthly_rate = self.int_rate/12
        return (self.loan_amount *  monthly_rate * (1 + monthly_rate)**n / ((1 + monthly_rate)**n - 1))
        
def _test():
    #
    loan_amount = 240000
    int_rate = 0.05
    mortgage_term = 30

    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print(mtgCalc.calc_level_payment())
    print(mtgCalc.compute_level_payment_analytically())

if __name__ == "__main__":
    _test()
