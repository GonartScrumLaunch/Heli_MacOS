from tkinter import ttk
import tkinter as tk
import Adventures.Adventure_0 as Seat_0
import Adventures.Adventure_1 as Seat_1
import Adventures.Adventure_2 as Seat_2
import Adventures.Adventure_3 as Seat_3
import Adventures.Adventure_4 as Seat_4
import Adventures.Adventure_5 as Seat_5
import Adventures.Adventure_6 as Flat_6
import Adventures.Adventure_7 as Flat_7
import Adventures.Adventure_8 as Flat_8
import Adventures.Adventure_9 as Flat_9
import Adventures.Adventure_10 as Flat_10
import Adventures.Adventure_11 as Flat_11
import Adventures.Adventure_12 as Accommodation_12
import UIExt as ui

TypeAdventures = ("Seat Pricing Multiday Lodging", "Seat Pricing Multiday NoLodging", "Seat Pricing Nightly Rate Lodging",
                  "Seat Pricing Daily Rate Lodging", "Seat Pricing Daily Rate NoLodging", "Seat Pricing Single Day NoLodging",
                  "Accommodation Pricing Multiday Lodging", "Accomm_Nightly_aL", "Accomm_Daily_aL", "Flat Rate Pricing Multiday Lodging",
                  "Flat Rate Pricing Multiday NoLodging", "Flat Rate Pricing Nightly Lodging", "Flat Rate Pricing Daily Lodging",
                  "Flat Rate Pricing Daily NoLodging", "Flat Rate Pricing Single Day NoLodging")
Currency = ("USD", "BRL", "CAD", "NZD", "AUD", "EUR", "ISK", "MXN", "GBP", "INR", "CHF", "JPY")
win = tk.Tk()
win.config(bg='#A0A0A0')
win.title('Heli Manager')
win.geometry('800x400+10+10')
win.resizable(False, False)

adventures = {
    "Seat Pricing Nightly Rate Lodging": Seat_0.SeatNRL(),
    "Seat Pricing Daily Rate Lodging": Seat_1.SeatDRL(),
    "Seat Pricing Daily Rate NoLodging": Seat_2.SeatDRnoL(),
    "Seat Pricing Multiday Lodging": Seat_3.SeatMdL(),
    "Seat Pricing Multiday NoLodging": Seat_4.SeatMdnoL(),
    "Seat Pricing Single Day NoLodging": Seat_5.SeatSdnoL(),
    "Flat Rate Pricing Multiday Lodging": Flat_6.FlatMdL(),
    "Flat Rate Pricing Single Day NoLodging": Flat_7.FlatSdnoL(),
    "Flat Rate Pricing Multiday NoLodging": Flat_8.FlatMdnoL(),
    "Flat Rate Pricing Daily Lodging": Flat_9.FlatDL(),
    "Flat Rate Pricing Daily NoLodging": Flat_10.FlatRDnoL(),
    "Flat Rate Pricing Nightly Lodging": Flat_11.FlatNL(),
    "Accommodation Pricing Multiday Lodging": Accommodation_12.APMdL(),
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
