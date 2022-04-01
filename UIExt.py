import tkinter as tk

def int_element(window, text, x, y, label_width, entry_width, value=0):
    label = tk.Label(window, text=text, fg="#eee", bg="#000000", font=("Arial", "10"))
    label.place(x=x, y=y, height=30, width=label_width)
    ent = tk.Entry(window, textvariable=tk.IntVar(value=value), justify=tk.CENTER, font=("Arial", 10, "bold"), validate='key',
                   vcmd=int_validate(window))
    ent.place(x=x + label_width + 1, y=y, height=30, width=entry_width)
    return ent


def double_element(window, text, x, y, labelWidth, entryWidth, value=0.0):
    label = tk.Label(window, text=text, fg="#eee", bg="#000000", font=("Arial", "10"))
    label.place(x=x, y=y, height=30, width=labelWidth)
    ent = tk.Entry(window, textvariable=tk.DoubleVar(value=value), justify=tk.CENTER, font=("Arial", 10, "bold"), validate='key',
                   vcmd=float_validate(window))
    ent.place(x=x + labelWidth + 1, y=y, height=30, width=entryWidth)
    return ent, label


def checkbox_element(window, text, x, y, labelWidth, entryWidth, value, command):
    box = tk.IntVar()
    checkbox = tk.Checkbutton(window, text=text, variable=box, onvalue=0, offvalue=1, font=("Arial", 10),
                              command=command)
    checkbox.place(x=x, y=y, height=30, width=labelWidth)
    intvar = tk.IntVar(value=value)
    ent = tk.Entry(window, textvariable=intvar, justify=tk.CENTER, font=("Arial", 10, "bold"), validate='key',
                   vcmd=float_validate(window))
    ent.place(x=x + labelWidth + 1, y=y, height=30, width=entryWidth)
    return ent, checkbox, box

def label_element(window, text, x, y, height, labelWidth):
    label = tk.Label(window, text=text, fg="#FFFFFF", bg="#000000", font=("Arial", "11"))
    label.place(x=x, y=y, height=height, width=labelWidth)


def int_validate(window):
    def validate(inp):
        if inp == "":
            return True
        try:
            int(inp)
        except:
            return False
        return True

    return window.register(validate), '%P'


def float_validate(window):
    def validate(inp):
        if inp == "":
            return True
        try:
            float(inp)
        except:
            return False
        return True

    return window.register(validate), '%P'

