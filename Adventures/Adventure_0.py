import tkinter as tk
import Deposit
import Taxes
import UIExt as ui
import AddonsPanel


def show(*args):
    args = args[0]
    tax = Taxes.TaxesTable()
    deposit = Deposit.depPanel()
    addon = AddonsPanel.addons()
    calc = tk.Toplevel()
    photo2 = tk.PhotoImage(file=r"C:\Users\Legion\Desktop\heli_manager\HeliOS.png")
    calc.iconphoto(False, photo2)
    calc.config(bg='#A0A0A0')
    calc.title('Heli calculator')
    calc.geometry('1185x800+700+10')
    calc.resizable(False, False)

    label1calc = tk.Label(calc, text="Current adventure: " + args[0], fg="#eee",
                          bg="#115A36", font=("Arial", "10"))
    label1calc.place(x=30, y=33, height=30, width=355)
    label2calc = tk.Label(calc, text="Current currency: " + args[1], fg="#eee",
                          bg="#115A36", font=("Arial", "10"))
    label2calc.place(x=30, y=66, height=30, width=355)
    label3calc = tk.Label(calc, text="Processing Fee Rate,%: " + args[2], fg="#eee",
                          bg="#115A36", font=("Arial", "10"))
    label3calc.place(x=30, y=99, height=30, width=355)
    constant2 = tk.Label(calc, text="VARIABLE", fg="#eee", bg="#333", font=("Arial", 10))
    constant2.place(x=415, y=33, height=30, width=355)

    def privcheck():
        if box1.get() == 1:
            costTobookPr.configure(state='normal')
            PricePerson.configure(state='disabled')
        else:
            costTobookPr.configure(state='disabled')
            PricePerson.configure(state='normal')
            PricePerson['text'] = 0

    a = tk.IntVar()
    box1 = tk.IntVar()
    сbprivat = tk.Checkbutton(calc, text="COST TO BOOK PRIVATELY", variable=box1, onvalue=1, offvalue=0,
                              font=("Arial", 10), state=tk.NORMAL, command=privcheck)
    сbprivat.place(x=415, y=165, height=30, width=230)
    costTobookPr = tk.Entry(calc, textvariable=a, justify=tk.CENTER, font=("Arial", 10, "bold"), state=tk.DISABLED,
                            validate='key', vcmd=ui.int_validate(calc))
    costTobookPr.place(x=646, y=165, height=30, width=124)

    def disccheck():
        if box2.get() == 1:
            ExStayDiscPerc.configure(state='normal')
            ExtStDiscAmount.configure(state='disabled')
        else:
            ExStayDiscPerc.configure(state='disabled')
            ExtStDiscAmount.configure(state='normal')

    b = tk.DoubleVar()
    box2 = tk.IntVar()
    CheckButDics = tk.Checkbutton(calc, text="Extended Stay Discount, %", variable=box2, onvalue=1, offvalue=0,
                                  font=("Arial", 10), state=tk.NORMAL, command=disccheck)
    CheckButDics.place(x=415, y=231, height=30, width=230)
    ExStayDiscPerc = tk.Entry(calc, textvariable=b, justify=tk.CENTER, font=("Arial", 10, "bold"), state=tk.DISABLED,
                              validate='key', vcmd=ui.float_validate(calc))
    ExStayDiscPerc.place(x=646, y=231, height=30, width=124)

    NumOfNights = ui.int_element(calc, "Number of nights", 415, 66, 230, 124)
    NumOfguests = ui.int_element(calc, "Number of guests", 415, 99, 230, 124)
    PricePerson = ui.int_element(calc, "PRICE/PERSON", 415, 132, 230, 124)
    ExtStDiscAmount = ui.int_element(calc, "Extended Stay Discount, amount", 415, 198, 230, 124)

    def submit():
        depositValue = deposit.getData()
        NumOfNightsValue = int(NumOfNights.get())
        NumOfguestsValue = int(NumOfguests.get())
        PricePersonValue = int(PricePerson.get())
        ExtStDiscAmountValue = int(ExtStDiscAmount.get())
        ExStayDiscPercValue = float(ExStayDiscPerc.get())
        CostTobookPrValue = int(costTobookPr.get())
        DiscAmountValue = int(args[4])
        DiscInPercValue = int(args[5])
        FeeValue = float(args[2])

        """Формула и методы"""

        def get_lodging():
            if box1.get() == 0:
                return Lodging[0]
            else:
                return Lodging[1]

        def get_discount():
            if args[3] == 0:
                return Discount[0]
            else:
                return Discount[1]

        def get_ExStayDisc(BaseSubtotal):
            result = 0
            if box2.get() == 0:
                return ExStayDisc[0]
            else:
                result += float(ExStayDisc[1] / 100) * BaseSubtotal
            return result

        def get_addons():
            addondata = addon.get_data()
            result = 0
            for n in range(0, len(addondata)):
                result += int(addondata[n][0].get()) * int(addondata[n][1].get())
            return result

        def get_taxes(BaseSubtotalafterdiscounts):
            taxdata = tax.get_data()

            result = 0
            for n in range(0, len(taxdata)):
                if taxdata[n][0].get() == "Amount":
                    if taxdata[n][2].get() == 1:
                        result += int(taxdata[n][1].get()) * NumOfguestsValue
                        print("1", result)
                    if taxdata[n][3].get() == 1:
                        result += int(taxdata[n][1].get()) * NumOfNightsValue
                        print("2", result)
                    if taxdata[n][3].get() == 0 and taxdata[n][2].get() == 0:
                        result += int(taxdata[n][1].get())
                        print("3", result)
                else:
                    result += int(taxdata[n][1].get()) / 100 * BaseSubtotalafterdiscounts
            return result


        def get_SubTotalAddonsTaxDep(basesubtotalafterexstdisc, addons, taxes):
            result = 0
            value1 = basesubtotalafterexstdisc + addons + taxes
            value2 = basesubtotalafterexstdisc + addons
            if depositValue[2]['text'] == "ON":
                if depositValue[3] == 0:  # Активный чекбокс Депозит Amount, если onvalue=0, иначе offvalue=1
                    result += value1 - int(depositValue[0])
                    return result
                else:
                    if depositValue[4] == 0:  # Активынй чекбокс Collect taxes with the deposit?
                        result += value1 - (float(depositValue[1]) / 100 * value1)
                        return result
                    else:
                        result += (value2 - float(depositValue[1]) / 100 * value2) + taxes
                        return result
            else:
                result += value1
                return result

        ExStayDisc = [ExtStDiscAmountValue, ExStayDiscPercValue]
        Discount = [DiscAmountValue, DiscInPercValue]  # это купоны, либо 40$ , либо 60$ либо нет купона
        Lodging = [PricePersonValue * NumOfguestsValue, CostTobookPrValue]

        BaseSubtotal = NumOfNightsValue * get_lodging()
        BaseSubtotalafterExStDisc = BaseSubtotal - get_ExStayDisc(BaseSubtotal)
        BaseSubtotalafterdiscounts = BaseSubtotal - get_ExStayDisc(BaseSubtotal) - get_discount()
        GrandTotalwithDeposit = get_SubTotalAddonsTaxDep(BaseSubtotalafterExStDisc, get_addons(),
                                                         get_taxes(BaseSubtotalafterdiscounts))
        RemainingAmount = GrandTotalwithDeposit - get_discount()

        FinalPayment = int(RemainingAmount + (FeeValue / 100 * RemainingAmount) * 100) / 100

        lb2 = tk.Label(calc, text="Result: " + str(FinalPayment), fg="#eee", bg="#115A36", font=("Arial", 15, "bold"))
        lb2.place(x=500, y=710, height=50, width=200)

    submit_button1 = tk.Button(calc, text="Submit", background="#333", foreground="#eee", font=("Arial", 15, "bold"),
                               command=submit)
    submit_button1.place(x=500, y=650, height=50, width=200)

    addon.show(calc)
    deposit.show(calc)
    tax.show(calc)
    calc.mainloop()
