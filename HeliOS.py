from tkinter import ttk
import tkinter as tk
import Adventures.Adventure_0 as adventure_0
import Adventures.Adventure_1 as adventure_1
import Adventures.Adventure_2 as adventure_2
import Adventures.Adventure_3 as adventure_3
import Adventures.Adventure_4 as adventure_4
import Adventures.Adventure_5 as adventure_5
import UIExt as ui

TypeAdventures = ("Seat Pricing Multi-day Lodging", "Seat Pricing Multi-day NoLodging", "Seat Pricing Nightly Rate Lodging",
                  "Seat Pricing Daily Rate Lodging", "Seat Pricing Daily Rate NoLodging", "Seat Pricing Single Day NoLodging", "Accomm_Multi-day_aL",
                  "Accomm_Nightly_aL", "Accomm_Daily_aL", "Flat_Multi-day_L", "Flat_Multi-day_NoL", "Flat_Nightly_aL",
                  "Flat_Daily_L", "Flat_Daily_NoL", "Flat_SingleDay_aNoL")
Currency = ("USD", "BRL", "CAD", "NZD", "AUD", "EUR", "ISK", "MXN", "GBP", "INR", "CHF", "JPY")
win = tk.Tk()
win.config(bg='#A0A0A0')
win.title('Heli Manager')
win.geometry('800x400+10+10')
win.resizable(False, False)

adventures = {
    "Seat Pricing Nightly Rate Lodging": adventure_0.SeatNRL(),
    "Seat Pricing Daily Rate Lodging": adventure_1.SeatDRL(),
    "Seat Pricing Daily Rate NoLodging": adventure_2.SeatDRnoL(),
    "Seat Pricing Multi-day Lodging": adventure_3.SeatMdL(),
    "Seat Pricing Multi-day NoLodging": adventure_4.SeatMdnoL(),
    "Seat Pricing Single Day NoLodging": adventure_5.SeatSdnoL()
}

def submit(*args):
    try:
        adventures[args[0]].show([item for item in args])
    except KeyError:
        print("Формула не реализована для {0}".format(args[0]))


def naccheck():
    if box.get() == 0:
        ent['state'] = "disabled"
    else:
        ent['state'] = "normal"


fee = tk.DoubleVar(value=3.5)
box = tk.IntVar()

checkbox_fee = tk.Checkbutton(win, text="Disable change Processing Fee Rate", variable=box, onvalue=0, offvalue=1,
                              font=("Arial", 10), command=naccheck)
checkbox_fee.place(x=420, y=99, height=30, width=301)
checkbox_fee.select()
ent = tk.Entry(win, textvariable=fee, justify=tk.CENTER, font=("Arial", 10, "bold"), validate='key',
               vcmd=ui.float_validate(win), state='disabled')
ent.place(x=571, y=66, height=30, width=150)


def DiscAmountCommand():
    if DiscAmount[2].get() == 0:
        DiscPerc[0]['state'] = "disabled"
        DiscAmount[0]['state'] = "normal"
    else:
        DiscAmount[0]['state'] = "disabled"
        DiscPerc[0]['state'] = "normal"


DiscPerc = ui.double_element(win, "Discount in % ($)", 420, 132, 150, 150, 60)
DiscAmount = ui.checkbox_element(win, "Discount Amount ($)", 420, 165, 150, 150, 40, DiscAmountCommand)
DiscAmount[1].deselect()
DiscAmount[0]['state'] = "disabled"

tk.Label(win, text="Type Adventure:", fg="#eee", bg="#000000", font=("Arial", "10")).place(x=29, y=66, height=30, width=110)
Dropdown_1 = ttk.Combobox(win, values=TypeAdventures, state='readonly')
Dropdown_1.place(x=140, y=66, height=30, width=250)
tk.Label(text="Currency:", fg="#eee", bg="#000000", font=("Arial", "10")).place(x=29, y=99, height=30, width=110)
tk.Label(text="CONSTANT", fg="#eee", bg="#000000", font=("Arial", 10)).place(x=420, y=33, height=30, width=301)
tk.Label(text="Processing Fee Rate,%:", fg="#eee", bg="#000000", font=("Arial", 10)).place(x=420, y=66, height=30, width=150)
Dropdown_2 = ttk.Combobox(win, values=Currency, state='readonly')
Dropdown_2.current(0)
Dropdown_2.place(x=140, y=99, height=30, width=250)

SubmitButton = tk.Button(win, text="Confirm", bg="#66FFB2", fg="#000000", borderwidth=5,
                         font=("Arial", 15, "bold"), command=lambda: submit(Dropdown_1.get(), Dropdown_2.get(),
                                                                            ent.get(), DiscAmount[2].get(),
                                                                            DiscAmount[0].get(), DiscPerc[0].get()))
SubmitButton.place(x=340, y=300, height=50, width=120)

win.mainloop()
