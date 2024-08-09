from tkinter import *
from mtgCalculator_AP import MortgageCalculator





#functions

def calc_level_payment():
    pass

    loanAmount = lbl_loanAmount.get()
    #mtgCalc = MortgageCalculator()

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

btn_enter = Button(window, text = "Calculate")
btn_enter.pack()



window.mainloop()
