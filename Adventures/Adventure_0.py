import tkinter as tk
import Deposit
import Taxes
import UIExt as ui
import AddonsPanel



class SeatNRL:
    def show(self, *args):
        self.args = args[0]
        self.tax = Taxes.TaxesTable()
        self.deposit = Deposit.depPanel()
        self.addons = AddonsPanel.Addons()
        self.calc = tk.Toplevel()
        self.calc.config(bg='#A0A0A0')
        self.calc.title('Heli calculator')
        self.calc.geometry('1185x800+700+10')
        self.calc.resizable(False, False)

        label1calc = tk.Label(self.calc, text="Current adventure: " + self.args[0], fg="#eee",
                              bg="#115A36", font=("Arial", "10"))
        label1calc.place(x=30, y=33, height=30, width=355)
        label2calc = tk.Label(self.calc, text="Current currency: " + self.args[1], fg="#eee",
                              bg="#115A36", font=("Arial", "10"))
        label2calc.place(x=30, y=66, height=30, width=355)
        label3calc = tk.Label(self.calc, text="Processing Fee Rate,%: " + self.args[2], fg="#eee",
                              bg="#115A36", font=("Arial", "10"))
        label3calc.place(x=30, y=99, height=30, width=355)
        constant2 = tk.Label(self.calc, text="VARIABLE", fg="#eee", bg="#333", font=("Arial", 10))
        constant2.place(x=415, y=33, height=30, width=355)

        a = tk.IntVar()
        self.box1 = tk.IntVar()
        check_button_cost_book = tk.Checkbutton(self.calc, text="COST TO BOOK PRIVATELY", variable=self.box1, onvalue=1, offvalue=0,
                                                font=("Arial", 10), state=tk.NORMAL, command=self.privcheck)
        check_button_cost_book.place(x=415, y=165, height=30, width=230)
        self.costTobookPr = tk.Entry(self.calc, textvariable=a, justify=tk.CENTER, font=("Arial", 10, "bold"), state=tk.DISABLED,
                                     validate='key', vcmd=ui.int_validate(self.calc))
        self.costTobookPr.place(x=646, y=165, height=30, width=124)

        b = tk.DoubleVar()
        self.box2 = tk.IntVar()
        check_button_discount = tk.Checkbutton(self.calc, text="Extended Stay Discount, %", variable=self.box2, onvalue=1, offvalue=0,
                                               font=("Arial", 10), state=tk.NORMAL, command=self.disccheck)
        check_button_discount.place(x=415, y=231, height=30, width=230)
        self.ExStayDiscPerc = tk.Entry(self.calc, textvariable=b, justify=tk.CENTER, font=("Arial", 10, "bold"), state=tk.DISABLED,
                                       validate='key', vcmd=ui.float_validate(self.calc))
        self.ExStayDiscPerc.place(x=646, y=231, height=30, width=124)

        self.NumOfNights = ui.int_element(self.calc, "Number of nights", 415, 66, 230, 124)
        self.NumOfguests = ui.int_element(self.calc, "Number of guests", 415, 99, 230, 124)
        self.PricePerson = ui.int_element(self.calc, "PRICE/PERSON", 415, 132, 230, 124)
        self.ExtStDiscAmount = ui.int_element(self.calc, "Extended Stay Discount, amount", 415, 198, 230, 124)

        submit_button1 = tk.Button(self.calc, text="Confirm", bg="#66FFB2", fg="#000000", font=("Arial", 15, "bold"),
                                   borderwidth=7, command=self.submit)
        submit_button1.place(x=500, y=530, height=50, width=200)


        self.addons.show(self.calc)
        self.deposit.show(self.calc)
        self.tax.show(self.calc)
        self.calc.mainloop()

    def privcheck(self):
        if self.box1.get() == 1:
            self.costTobookPr.configure(state='normal')
            self.PricePerson.configure(state='disabled')
        else:
            self.costTobookPr.configure(state='disabled')
            self.PricePerson.configure(state='normal')
            self.PricePerson['text'] = 0


    def disccheck(self):
        if self.box2.get() == 1:
            self.ExStayDiscPerc.configure(state='normal')
            self.ExtStDiscAmount.configure(state='disabled')
        else:
            self.ExStayDiscPerc.configure(state='disabled')
            self.ExtStDiscAmount.configure(state='normal')


    def submit(self):
        self.depositValue = self.deposit.getData()
        self.NumOfNightsValue = int(self.NumOfNights.get())
        self.NumOfguestsValue = int(self.NumOfguests.get())
        self.PricePersonValue = int(self.PricePerson.get())
        self.ExtStDiscAmountValue = int(self.ExtStDiscAmount.get())
        self.ExStayDiscPercValue = float(self.ExStayDiscPerc.get())
        self.CostTobookPrValue = int(self.costTobookPr.get())
        self.DiscAmountValue = int(self.args[4])
        self.DiscInPercValue = int(self.args[5])
        fee_value = float(self.args[2])

        """Списки значений, формулы и финальные лейблы"""

        self.ExStayDisc = [self.ExtStDiscAmountValue, self.ExStayDiscPercValue]
        self.Discount = [self.DiscAmountValue, self.DiscInPercValue]  # это купоны, либо 40$ , либо 60$ либо нет купона
        self.Lodging = [self.PricePersonValue * self.NumOfguestsValue, self.CostTobookPrValue]


        self.BaseSubtotal = self.NumOfNightsValue * self.get_lodging()
        self.basesubtotal_after_ex_st_disc_dddons = self.BaseSubtotal - self.get_ExStayDisc() + self.get_addons()  # эта формула нужна, чтоб взять процентную таксу (без учёта discount)
        self.basesubtotal_after_discounts = self.BaseSubtotal - self.get_ExStayDisc() - self.get_discount()
        self.taxes = self.get_taxes()
        deposit_subtotal = self.get_SubTotalAddonsTaxDep()

        grand_total = self.basesubtotal_after_discounts + self.get_addons() + self.taxes[0]

        full_payment = float(grand_total - deposit_subtotal + (fee_value / 100) * grand_total)

        lb1 = tk.Label(self.calc, text="Tax Total: " + str(round(self.taxes[0], 3)), fg="#eee", bg="#115A36",
                       font=("Arial", 12, "bold"))
        lb1.place(x=475, y=590, height=30, width=250)

        lb2 = tk.Label(self.calc, text="Deposit Subtotal: " + str(round(deposit_subtotal, 3)), fg="#eee", bg="#115A36",
                       font=("Arial", 12, "bold"))
        lb2.place(x=475, y=630, height=30, width=250)

        lb3 = tk.Label(self.calc, text="Fee Total: " + str(round(fee_value / 100 * grand_total, 3)), fg="#eee",
                       bg="#115A36", font=("Arial", 12, "bold"))
        lb3.place(x=475, y=670, height=30, width=250)

        lb4 = tk.Label(self.calc, text="Full Payment: " + str(round(full_payment, 2)), fg="#000000", bg="#66FFB2",
                       font=("Arial", 15, "bold"))
        lb4.place(x=475, y=710, height=50, width=250)

    """Методы используемые для получения значений в формулы"""

    def get_lodging(self):
        if self.box1.get() == 0:
            return self.Lodging[0]
        else:
            return self.Lodging[1]

    def get_discount(self):
        if self.args[3] == 0:
            return self.Discount[0]
        else:
            return self.Discount[1]

    def get_ExStayDisc(self):
        result = 0
        if self.box2.get() == 0:
            return self.ExStayDisc[0]
        else:
            result += float(self.ExStayDisc[1] / 100) * self.BaseSubtotal
        return result

    def get_addons(self):
        self.addonsdata = self.addons.get_data()
        result = 0
        for n in range(0, len(self.addonsdata)):
            result += int(self.addonsdata[n][0].get()) * int(self.addonsdata[n][1].get())
        return result

    def get_taxes(self):
        self.taxdata = self.tax.get_data()
        result = 0
        self.taxpercamount = 0
        for n in range(0, len(self.taxdata)):
            if self.taxdata[n][0].get() == "Amount":
                if self.taxdata[n][2].get() == 1:
                    result += int(self.taxdata[n][1].get()) * self.NumOfguestsValue
                if self.taxdata[n][3].get() == 1:
                    result += int(self.taxdata[n][1].get()) * self.NumOfNightsValue
                if self.taxdata[n][3].get() == 0 and self.taxdata[n][2].get() == 0:
                    result += int(self.taxdata[n][1].get())
            else:
                result += int(self.taxdata[n][1].get()) / 100 * self.basesubtotal_after_discounts
                self.taxpercamount += int(self.taxdata[n][1].get())
        return result, self.taxpercamount


    def get_SubTotalAddonsTaxDep(self):
        result = 0
        self.DepositTaxAmount = 0
        self.DepositAmount = 0
        if self.depositValue[2]['text'] == "ON":
            if self.depositValue[3] == 0:  # Активный чекбокс Депозит Amount, если onvalue=0, иначе offvalue=1
                if self.depositValue[4] == 0:  # Активынй чекбокс Collect taxes with the deposit?
                    self.DepositTaxAmount += int(self.depositValue[0]) * (self.taxpercamount / 100)
                    result += int(self.depositValue[0]) + self.DepositTaxAmount
                    return result
                else:
                    result += int(self.depositValue[0])
                    return result
            else:
                self.DepositAmount += self.basesubtotal_after_ex_st_disc_dddons * (float(self.depositValue[1]) / 100)
                self.DepositTaxAmount += (self.BaseSubtotal - self.get_ExStayDisc()) * (float(self.depositValue[1]) / 100) * (self.taxpercamount / 100)
                result += self.DepositAmount + self.DepositTaxAmount
                return result
        else:
            return result


