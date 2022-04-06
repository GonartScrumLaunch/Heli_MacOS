import tkinter as tk
import UIExt as ui


class depPanel:
    def toggle(self):
        if self.toggle_button['text'] == 'ON':
            self.toggle_button['text'] = 'OFF'
            self.DepositPerc[0].place(width=0, height=0)
            self.DepositPerc[1].place(width=0, height=0)
            self.DepositAmount[0].place(width=0, height=0)
            self.DepositAmount[1].place(width=0, height=0)
            self.collecttaxes.place(width=0, height=0)
        else:
            self.toggle_button['text'] = 'ON'
            self.DepositPerc[0].place(width=124, height=30)
            self.DepositPerc[1].place(width=230, height=30)
            self.DepositAmount[0].place(width=124, height=30)
            self.DepositAmount[1].place(width=230, height=30)
            self.collecttaxes.place(width=355, height=30)

    def show(self, window):
        self.toggle_button = tk.Button(window, text='ON', borderwidth=5, command=self.toggle)
        self.toggle_button.place(x=415, y=264, height=30, width=177)
        SwitchLabel = tk.Label(window, text="DEPOSIT POLICY ", fg="#eee", bg="#000000", )
        SwitchLabel.place(x=593, y=264, height=30, width=177)
        self.DepositPerc = ui.double_element(window, "Deposit, % ", 415, 297, 230, 124)
        self.DepositAmount = ui.checkbox_element(window, "Deposit, amount", 415, 330, 230, 124, 0, self.deposit_check)
        self.DepositPerc[0]['state'] = 'disabled'
        self.DepositAmount[1].select()

        self.boxcollect = tk.IntVar()
        self.collecttaxes = tk.Checkbutton(window, text="Collect taxes with the deposit?", variable=self.boxcollect,
                                           onvalue=0, offvalue=1, font=("Arial", 10))
        self.collecttaxes.place(x=415, y=363, height=30, width=355)
        self.collecttaxes.deselect()


    def getData(self):
        return self.DepositAmount[0].get(), self.DepositPerc[0].get(), self.toggle_button, self.DepositAmount[2].get(),\
               self.boxcollect.get()

    def deposit_check(self):
        if self.DepositAmount[2].get() == 1:  #  если onvalue=0, иначе offvalue=1
            self.DepositAmount[0]['state'] = 'disabled'
            self.DepositPerc[0]['state'] = 'normal'
            self.collecttaxes.place(width=0, height=0)
        else:
            self.DepositAmount[0]['state'] = 'normal'
            self.DepositPerc[0]['state'] = 'disabled'
            self.collecttaxes.place(width=355, height=30)


