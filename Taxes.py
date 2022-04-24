import tkinter as tk
from tkinter import ttk
import UIExt as ui

class TaxesTable:
    def __init__(self):
        self.array_label_tax = []
        self.array_dropdown = []
        self.array_price = []
        self.array_delete = []
        self.array_checkbox_pers = []
        self.array_checkbox_cycle = []
        self.array_checkvars = []
        self.TaxType = ("Percentage", "Amount")

    def get_data(self):
        result = []
        for n in range(0, len(self.array_delete)):
            result.append((self.array_dropdown[n], self.array_price[n], self.array_checkvars[n][0], self.array_checkvars[n][1]))
        return result


    def show(self, widget):
        tk.Label(widget, text="TAXES", fg="#eee", bg="#000000", font=("Arial", 10)).place(x=800, y=33, height=30, width=355)
        tk.Button(widget, text="Add Taxes", background="#66FFB2", foreground="#000000", font=("Arial", 12),
                  command=lambda: self.addtax(widget)).place(x=800, y=66, height=30, width=355)

    def callbackFunc(self, event):
        self.rebuild()

    def rebuild(self):
        lendth = 99
        for n in range(0, len(self.array_delete)):
            y = lendth + n * 33
            self.array_delete[n]['command'] = lambda l = n: self.remove(l)
            self.array_dropdown[n].place(x=886, y=y, height=30, width=85)
            self.array_price[n].place(x=972, y=y, height=30, width=82)
            self.array_label_tax[n].place(x=800, y=y, height=30, width=85)
            self.array_delete[n].place(x=1055, y=y, height=30, width=100)
            if self.array_dropdown[n].get() == "Amount":
                lendth += 33
                self.array_checkbox_pers[n].place(x=800, y=y + 33, height=30, width=175)
                self.array_checkbox_cycle[n].place(x=980, y=y + 33, height=30, width=175)
            else:
                self.array_checkbox_pers[n].place(x=0, y=0, height=0, width=0)
                self.array_checkbox_cycle[n].place(x=0, y=0, height=0, width=0)


    def remove(self, index):
        if len(self.array_delete) != 0:
            self.array_dropdown[index].destroy()
            self.array_price[index].destroy()
            self.array_label_tax[index].destroy()
            self.array_label_tax.pop(index)
            self.array_price.pop(index)
            self.array_dropdown.pop(index)
            self.array_delete[index].destroy()
            self.array_delete.pop(index)
            self.array_checkbox_pers[index].destroy()
            self.array_checkbox_pers.pop(index)
            self.array_checkbox_cycle[index].destroy()
            self.array_checkbox_cycle.pop(index)
            self.array_checkvars.pop(index)
            self.rebuild()


    def addtax(self, widget):
        if len(self.array_delete) < 10:
            self.array_label_tax.append(tk.Label(widget, text=self.get_name(), fg="#eee", bg="#000000", font=("Arial", 10)))
            dropdown = ttk.Combobox(widget, values=self.TaxType, state='readonly')
            dropdown.current(0)
            dropdown.bind('<<ComboboxSelected>>', self.callbackFunc)
            self.array_dropdown.append(dropdown)
            entry = tk.Entry(widget, validate='all', textvariable=tk.IntVar(value=0),
                             justify=tk.CENTER, vcmd=ui.float_validate(widget))
            self.array_price.append(entry)
            bool_var_pers = tk.BooleanVar()
            bool_var_cycle = tk.BooleanVar()
            self.array_checkvars.append((bool_var_pers, bool_var_cycle))
            self.array_checkbox_pers.append(tk.Checkbutton(widget, text="Per Person", font=("Arial", 10),
                                                           state=tk.ACTIVE, variable=bool_var_pers))
            self.array_checkbox_cycle.append(tk.Checkbutton(widget, text="Per Night/Day/Unit", font=("Arial", 10),
                                                            state=tk.ACTIVE, variable=bool_var_cycle))
            self.array_delete.append(tk.Button(widget, text="Delete", background="#FA0F0F", foreground="#000000",
                                               font=("Arial", 12)))
            self.rebuild()


    def get_name(self):
        for n in range(0, len(self.array_delete) + 1):
            if self.is_aviable(n) == 1:
                return "Tax №" + str(n + 1)

    def is_aviable(self, index):
        name = "Tax №" + str(index + 1)
        for n in range(0, len(self.array_delete)):
            if name == self.array_label_tax[n]['text']:
                return 0
        return 1










