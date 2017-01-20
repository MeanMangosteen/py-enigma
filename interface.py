#!/usr/bin/python3

from tkinter import *
from tkinter import ttk

rotor_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']


class Menu(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.unselected_rotors = ttk.Frame(parent)
        self.unselected_rotors.grid()
        self.selected_rotors = []

        self.rotor_buttons = []

        self.rotor_text = ttk.Label(self.unselected_rotors, text='Rotors').grid(column=0, row=0, columnspan=3, sticky=(N))
        self.i = 0
        for rotor in rotor_list:
            self.button = ttk.Button(self.unselected_rotors, text=rotor,
                                     command=lambda a=self.i: self.rotor_click(a))
            self.rotor_buttons.append(self.button)
            self.i += 1
        rotor_indicies = list(range(0, len(self.rotor_buttons)))
        row_index = 1
        column_multiplier = 0
        for i, btn in zip(rotor_indicies, self.rotor_buttons):
            i -= (column_multiplier * 3)

            print("col: {}, row: {}".format(i, row_index))
            btn.grid(column=i, row=row_index)
            if i == 2:
                column_multiplier += 1
                row_index += 1

        self.label_text = ttk.Label(self.unselected_rotors, text='Reflectors').grid(column=4, row=0, columnspan=2)
        self.reflector_b = ttk.Button(self.unselected_rotors, text='B').grid(column=4, row=1)
        self.reflector_c = ttk.Button(self.unselected_rotors, text='C').grid(column=5, row=1)
        self.ring_setting_text = ttk.Label(self.unselected_rotors, text='Ring Setting').grid(column=6, row=0)
        self.ring_setting = ttk.Entry(self.unselected_rotors, text="hello").grid(column=6, row=1)
        self.ring_setting_text = ttk.Label(self.unselected_rotors, text='Initial Position').grid(column=6, row=2)
        self.initial_setting = ttk.Entry(self.unselected_rotors).grid(column=6, row=3)
        self.ring_setting_text = ttk.Label(self.unselected_rotors, text='Plugboard').grid(column=0, row=4, columnspan=6)
        self.plugboard = ttk.Entry(self.unselected_rotors, width=50).grid(column=0, row=5, columnspan=6)

    def rotor_click(self, i):
        self.selected_rotors.append(self.rotor_buttons[i]['text'])
        print(self.selected_rotors)

if __name__ == "__main__":
    root = Tk()
    Menu(root)
    root.mainloop()


def destroy_btn(btn):
    btn.grid_forget()
