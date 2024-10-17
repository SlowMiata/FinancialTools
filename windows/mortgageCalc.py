from tkinter import *
import sys
import os

# Step 2: Get the parent directory path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Step 4: Append the parent directory to sys.path
sys.path.append(parent_dir)

from mtgCalculator_AP import MortgageCalculator



#functions

def calc_level_payment():
    # Get input values and remove leading/trailing spaces
    loanAmount = ent_loanAmount.get().strip()
    interestRate = ent_interestRate.get().strip()
    term = ent_mortgageTerm.get().strip()

    # 1. Check for empty or whitespace-only inputs
    if not loanAmount or not interestRate or not term:
        lbl_error.config(text="Please fill out all boxes")
        return

    # 2. Validate if loan amount and term are digits
    if not loanAmount.isdigit() or not term.isdigit():
        lbl_error.config(text="Loan amount and term must be whole numbers")
        return

    # 3. Validate if interest rate is a valid float
    try:
        interestRate = float(interestRate)
    except ValueError:
        lbl_error.config(text="Interest rate must be a valid decimal number")
        return

    # 4. Ensure input values are within logical ranges
    loanAmount = int(loanAmount)
    term = int(term)

    if loanAmount <= 0:
        lbl_error.config(text="Loan amount must be greater than 0")
        return

    if interestRate <= 0 or interestRate >= 1:
        lbl_error.config(text="Interest rate must be between 0 and 1 (e.g., 0.05 for 5%)")
        return

    if term <= 0:
        lbl_error.config(text="Term must be greater than 0")
        return

    if loanAmount > 1_000_000_000:
        lbl_error.config(text="Loan amount too large")
        return

    if term > 1200:  # Example: No mortgage term longer than 100 years
        lbl_error.config(text="Term is too long (max 1200 months)")
        return

    # 5. Calculate and display the monthly payment if all checks pass
    lbl_error.config(text="")  # Clear any previous error message
    mtgCalc = MortgageCalculator(loan_amount=loanAmount, int_rate=interestRate, term=term)
    
    try:
        result = mtgCalc.calc_level_payment()  # Handle potential division by zero
        lbl_total.config(text=f"Monthly Payment: {result:.2f}")
    except ZeroDivisionError:
        lbl_error.config(text="Calculation error: Check your input values")
        
##predefined font
large_font = ("Helvetica", 30)

##main frame
window = Tk()
window.title("Mortgage Calculator")
window.geometry("1000x800")
window.resizable(width=False, height= False)

lbl_levelPayment = Label(master=window, text = "Calculate level payment",font=large_font)
lbl_levelPayment.pack()


##input frames
frm_inputs = Frame(window, relief= RAISED)
frm_inputs.pack()

##loan amount input
lbl_loanAmount = Label(master = frm_inputs,text="Enter Loan Amount:")
ent_loanAmount = Entry(master = frm_inputs)

lbl_loanAmount.grid(row = 0, column= 0, sticky= 'e')
ent_loanAmount.grid(row = 0, column= 1 , sticky= "w")

#interest rate input
lbl_interestRate = Label(master = frm_inputs,text="Enter interest rate (decimal form):")
ent_interestRate = Entry(master = frm_inputs)

lbl_interestRate.grid(row= 1, column= 0, sticky= "e")
ent_interestRate.grid(row = 1, column= 1, sticky= "w")

#mortgage term input
lbl_mortgageTerm = Label(master = frm_inputs,text="Enter mortgage term (in months):")
ent_mortgageTerm = Entry(master = frm_inputs)

lbl_mortgageTerm.grid(row= 2, column= 0, sticky= "e")
ent_mortgageTerm.grid(row = 2, column= 1, sticky= "w")


#calculate button
btn_enter = Button(window, text = "Calculate", command= calc_level_payment)
btn_enter.pack()


#monthly payment option
lbl_total = Label()
lbl_total.pack()

#error display
lbl_error = Label()
lbl_error.pack()

window.mainloop()


##OOP version
#creating the main class
# class App:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Mortgage Calculator")
#         self.master.geometry("1200x960")
#         self.master.resizable (width = False, height = False)