import tkinter as tk
import UIExt as ui

class Addons:


    def __init__(self):
        self.array_count = []
        self.array_price = []
        self.array_label_count = []
        self.array_label_price = []

        self.count = 0

    def add(self, widget):
        if self.count < 10:
            y = 165 + self.count * 33
            lcalc = tk.Label(widget, text="Num Of Addons " + str(self.count+1), fg="#eee", bg="#333", font=("Arial", "10"))
            lcalc.place(x=30, y=y, height=30, width=125)
            self.array_label_count.append(lcalc)
            self.array_count.append(tk.Entry(widget, validate='key', justify=tk.CENTER,
                                             textvariable=tk.IntVar(value=0),
                                             vcmd=ui.int_validate(widget))) # Create and append to list
            self.array_count[self.count].place(x=156, y=y, height=30, width=50) # Place the just created widget
            lcalc = tk.Label(widget, text="Price Of Addons", fg="#eee", bg="#333", font=("Arial", "10"))
            lcalc.place(x=207, y=y,  height=30, width=125)
            self.array_label_price.append(lcalc)
            self.array_price.append(tk.Entry(widget, validate='key', justify=tk.CENTER, textvariable=tk.IntVar(value=0),
                                             vcmd=ui.int_validate(widget)))  # Create and append to list
            self.array_price[self.count].place(x=332, y=y, height=30, width=52)
            self.count += 1

    def get_data(self):
        result = []
        for n in range(0, len(self.array_price)):
            result.append((self.array_count[n], self.array_price[n]))
        return result

    def remove(self):
        if self.count != 0:
            self.array_count[self.count-1].destroy()
            self.array_price[self.count-1].destroy()
            self.array_label_price[self.count-1].destroy()
            self.array_label_count[self.count-1].destroy()
            self.array_label_count.pop(self.count-1)
            self.array_price.pop(self.count-1)
            self.array_count.pop(self.count-1)
            self.array_label_price.pop(self.count-1)
            self.count -= 1


    def show(self, widget):
        btn = tk.Button(widget, text=" + Add add-ons", background="#555", foreground="#ccc", font=("Arial", 12),
                        command=lambda: self.add(widget))
        btn2 = tk.Button(widget, text=" - Remove add-ons", background="#555", foreground="#ccc", font=("Arial", 12),
                         command=self.remove)

        btn.place(x=30, y=132, height=30, width=175)
        btn2.place(x=210, y=132, height=30, width=175)
