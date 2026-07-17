import tkinter as tk
from tkinter import filedialog
import json
import random
import customtkinter
import os

root = customtkinter.CTk()
root.title('Sweatbox Aircraft')
root.attributes('-topmost', True)
root.geometry(f"{520}x{70}")

data = {'departures': [], 'arrivals': []}
arrivals_iterator = iter(data['arrivals'])
# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


def choose_file():
    global data, arrivals_iterator
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            # Read JSON file.
            data = json.load(file)
            arrivals_iterator = iter(data['arrivals'])

        button1.destroy()  # Hide the "Choose File" button after a file is chosen.
        button2.grid(row=1, column=1)  # Show the "Next" buttons.
        button3.grid(row=2, column=1)  # Show the "Next" buttons.
        root.title(f"Sweatbox Aircraft: {os.path.basename(filename)}")
        display_info()


def display_info():
    load_next_departure()
    load_next_arrival()


def load_next_departure():
    departures = data.get('departures', [])
    if departures:
        i = random.randrange(len(departures))
        label_departure = departures.pop(i)
    else:
        label_departure = "No more departures."
    lbl_departure.configure(text=f"   Departure: {label_departure}     ")


def load_next_arrival():
    global arrivals_iterator
    try:
        label_arrival = next(arrivals_iterator)
    except StopIteration:
        label_arrival = "No more arrivals."
    lbl_arrival.configure(text=f"   Arrival: {label_arrival}     ")


button1 = customtkinter.CTkButton(root, text="Choose File", command=choose_file)
button1.place(relx=0.5, rely=0.5, anchor='center')
# button1.grid(row=0, column=0, columnspan=2)  # Button will span 2 columns.

lbl_departure = customtkinter.CTkLabel(root, text="")
lbl_departure.grid(row=1, column=0)

button2 = customtkinter.CTkButton(root, text="Next Departure", command=load_next_departure, height=2)
button2.grid(row=1, column=2)
button2.grid_remove()  # Initial hide.

lbl_arrival = customtkinter.CTkLabel(root, text="")
lbl_arrival.grid(row=2, column=0)

button3 = customtkinter.CTkButton(root, text="Next Arrival", command=load_next_arrival, height=2)
button3.grid(row=2, column=2)
button3.grid_remove()  # Initial hide.
root.mainloop()
