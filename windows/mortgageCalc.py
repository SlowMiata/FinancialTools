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
    
    #need to check if the user has enter a character other than numbers
    #need to check if the user has enter nothing

    loanAmount = ent_loanAmount.get().strip()
    
    interestRate = ent_interestRate.get().strip()
    term = ent_mortgageTerm.get().strip()
    
    
    
    if loanAmount == "" or interestRate == "" or term == "":
        lbl_error["text"] = "Please fill out all boxes"
    
    elif not loanAmount.isdigit() or not term.isdigit():
        lbl_error["text"] = "Please enter only numbers"
    else:
        lbl_error["text"] = ""
        loanAmount = int(loanAmount)
        interestRate = float(interestRate)
        term = int(term)
        mtgCalc = MortgageCalculator(loan_amount= loanAmount, int_rate= interestRate, term= term)
        lbl_total["text"] = f"{mtgCalc.calc_level_payment()}"
        
##predefined
large_font = ("Helvetica", 16)

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

lbl_loanAmount = Label(master = frm_inputs,text="Enter Loan Amount:")
ent_loanAmount = Entry(master = frm_inputs)


lbl_loanAmount.grid(row = 0, column= 0, sticky= 'e')
ent_loanAmount.grid(row = 0, column= 1 , sticky= "w")

lbl_interestRate = Label(master = frm_inputs,text="Enter interest rate (decimal form):")
ent_interestRate = Entry(master = frm_inputs)

lbl_interestRate.grid(row= 1, column= 0, sticky= "e")
ent_interestRate.grid(row = 1, column= 1, sticky= "w")

lbl_mortgageTerm = Label(master = frm_inputs,text="Enter mortgage term (in months):")
ent_mortgageTerm = Entry(master = frm_inputs)

lbl_mortgageTerm.grid(row= 2, column= 0, sticky= "e")
ent_mortgageTerm.grid(row = 2, column= 1, sticky= "w")

btn_enter = Button(window, text = "Calculate", command= calc_level_payment)
btn_enter.pack()

lbl_total = Label()
lbl_total.pack()

lbl_error = Label()
lbl_error.pack()




window.mainloop()
