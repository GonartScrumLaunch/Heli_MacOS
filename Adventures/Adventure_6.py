import tkinter as tk
import Deposit
import Taxes
import UIExt as ui
import AddonsPanel


class FlatMdL:
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

        tk.Label(self.calc, text="Current adventure: " + self.args[0], fg="#eee",
                 bg="#115A36", font=("Arial", "10")).place(x=30, y=33, height=30, width=355)
        tk.Label(self.calc, text="Current currency: " + self.args[1], fg="#eee",
                 bg="#115A36", font=("Arial", "10")).place(x=30, y=66, height=30, width=355)
        tk.Label(self.calc, text="Processing Fee Rate,%: " + self.args[2], fg="#eee",
                 bg="#115A36", font=("Arial", "10")).place(x=30, y=99, height=30, width=355)
        tk.Label(self.calc, text="VARIABLE", fg="#eee", bg="#000000", font=("Arial", 10)).place(x=415, y=33, height=30,
                                                                                                width=355)
        self.NumOfNights = ui.int_element(self.calc, "Number of nights(per slot)", 415, 66, 230, 124)
        self.NumOfguests = ui.int_element(self.calc, "Number of guests", 415, 99, 230, 124)
        self.PricePerson = ui.int_element(self.calc, "PRICE/PERSON", 415, 132, 230, 124)
        tk.Label(self.calc, text='For this type of adventure, the fields: \n'
                                 'Number of nights(per slot) and Number of guests\n'
                                 'are used to calculate Taxes Amount', fg="#FFFFFF", justify='left',
                 font=("Arial", "10"), bg='#115A36').place(x=415, y=165, height=96, width=355)

        tk.Button(self.calc, text="Confirm", bg="#66FFB2", fg="#000000", font=("Arial", 15, "bold"),
                  borderwidth=7, command=self.submit).place(x=500, y=530, height=50, width=200)

        self.addons.show(self.calc)
        self.deposit.show(self.calc)
        self.tax.show(self.calc)
        self.calc.mainloop()


    def submit(self):
        self.depositValue = self.deposit.getData()
        self.NumOfNightsValue = int(self.NumOfNights.get())
        self.NumOfguestsValue = int(self.NumOfguests.get())
        self.PricePersonValue = int(self.PricePerson.get())
        self.DiscAmountValue = int(self.args[4])
        self.DiscInPercValue = int(self.args[5])
        fee_value = float(self.args[2])

        """Списки значений, формулы и финальные лейблы"""

        self.Discount = [self.DiscAmountValue, self.DiscInPercValue]  # это купоны, либо 40$ , либо 60$ либо нет купона

        self.BaseSubtotal = self.PricePersonValue
        self.basesubtotal_after_addons = self.BaseSubtotal + self.get_addons()  # эта формула нужна, чтоб взять процентную таксу (без учёта discount)
        self.basesubtotal_after_discounts = self.BaseSubtotal - self.get_discount()
        self.taxes = self.get_taxes()
        self.deposit_payment = self.get_deposit_value()

        deposit_subtotal = self.get_SubTotalAddonsTaxDep()
        grand_total = self.basesubtotal_after_discounts + self.get_addons() + self.taxes[0]
        full_payment = float(grand_total + fee_value / 100 * grand_total)

        ui.label_element(self.calc, "Deposit payment: ", 30, 530, 45, 190)
        ui.label_element(self.calc, "Remaining payment: ", 250, 530, 45, 190)
        ui.label_element(self.calc, "Dep.% or amount: " + str(self.deposit_payment) + " $", 30, 590, 30, 190)
        ui.label_element(self.calc, "Tax deposit: " + str(round(deposit_subtotal[1], 3)) + " $", 30, 630, 30, 190)
        ui.label_element(self.calc, "Fee deposit: " + str(round(deposit_subtotal[0] * (fee_value / 100), 3)) + " $",
                         30, 670, 30, 190)
        ui.label_element(self.calc, "Summary: " + str(round(deposit_subtotal[0] + deposit_subtotal[0] *
                                                            (fee_value / 100), 3)) + " $", 30, 710, 50, 190)
        ui.label_element(self.calc, "Tax, amount: " + str(round(self.taxes[2], 3)) + " $", 250, 590, 30, 190)
        ui.label_element(self.calc, "Remaining tax,%: " + str(round(self.taxes[3] - deposit_subtotal[1], 3)) + " $", 250, 630,
                         30, 190)
        ui.label_element(self.calc, "Fee remaining: " + str(round((grand_total - deposit_subtotal[0]) *
                                                                  (fee_value / 100), 3)) + " $", 250, 670, 30, 190)
        ui.label_element(self.calc, "Summary: " + str(round((grand_total - deposit_subtotal[0]) +
                                                            (fee_value / 100 * (grand_total - deposit_subtotal[0])), 3))
                         + " $", 250, 710, 50, 190)

        tk.Label(self.calc, text="Tax Total: " + str(round(self.taxes[0], 3)) + " $", fg="#eee", bg="#115A36",
                 font=("Arial", 12, "bold")).place(x=475, y=590, height=30, width=250)

        tk.Label(self.calc, text="Deposit Subtotal: " + str(round(deposit_subtotal[0], 3)) + " $", fg="#eee",
                 bg="#115A36", font=("Arial", 12, "bold")).place(x=475, y=630, height=30, width=250)

        tk.Label(self.calc, text="Fee Total: " + str(round(fee_value / 100 * grand_total, 3)) + " $", fg="#eee",
                 bg="#115A36", font=("Arial", 12, "bold")).place(x=475, y=670, height=30, width=250)

        tk.Label(self.calc, text="Full Payment: " + str(round(full_payment, 3)) + " $", fg="#000000", bg="#66FFB2",
                 font=("Arial", 15, "bold")).place(x=475, y=710, height=50, width=250)

    """Методы используемые для получения значений в формулы"""


    def get_discount(self):
        if self.args[3] == 0:
            return self.Discount[0]
        else:
            return self.Discount[1]

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
        tax_amount = 0
        tax_perc = 0
        for n in range(0, len(self.taxdata)):
            if self.taxdata[n][0].get() == "Amount":
                if self.taxdata[n][2].get() == 1:
                    result += int(self.taxdata[n][1].get()) * self.NumOfguestsValue
                    tax_amount += int(self.taxdata[n][1].get()) * self.NumOfguestsValue
                if self.taxdata[n][3].get() == 1:
                    result += int(self.taxdata[n][1].get()) * self.NumOfNightsValue
                    tax_amount += int(self.taxdata[n][1].get()) * self.NumOfNightsValue
                if self.taxdata[n][3].get() == 0 and self.taxdata[n][2].get() == 0:
                    result += int(self.taxdata[n][1].get())
                    tax_amount += int(self.taxdata[n][1].get())
            else:
                result += int(self.taxdata[n][1].get()) / 100 * self.basesubtotal_after_discounts
                self.taxpercamount += int(self.taxdata[n][1].get())
                tax_perc += int(self.taxdata[n][1].get()) / 100 * self.basesubtotal_after_discounts
        return result, self.taxpercamount, tax_amount, tax_perc

    def get_SubTotalAddonsTaxDep(self):
        result = 0
        self.DepositTaxAmount = 0
        self.DepositAmount = 0
        if self.depositValue[2]['text'] == "ON":
            if self.depositValue[3] == 0:  # Активный чекбокс Депозит Amount, если onvalue=0, иначе offvalue=1
                if self.depositValue[4] == 0:  # Активный чекбокс Collect taxes with the deposit?
                    self.DepositTaxAmount += int(self.depositValue[0]) * (self.taxpercamount / 100)
                    result += int(self.depositValue[0]) + self.DepositTaxAmount
                    return result, self.DepositTaxAmount
                else:
                    result += int(self.depositValue[0])
                    return result, self.DepositTaxAmount
            else:
                self.DepositAmount += self.basesubtotal_after_addons * (float(self.depositValue[1]) / 100)
                self.DepositTaxAmount += (self.BaseSubtotal * (float(self.depositValue[1]) / 100)) * \
                                         (self.taxpercamount / 100)
                result += self.DepositAmount + self.DepositTaxAmount
                return result, self.DepositTaxAmount
        else:
            return result, self.DepositTaxAmount

    def get_deposit_value(self):
        self.deposit_percentage = 0
        self.deposit_amount = 0
        if self.depositValue[3] == 0:
            self.deposit_amount += float(self.depositValue[0])
            return self.deposit_amount
        else:
            self.deposit_percentage += self.basesubtotal_after_addons * (float(self.depositValue[1]) / 100)
            return self.deposit_percentage
