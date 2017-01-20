#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import json

rotor_list = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']


class Menu(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.unselected_rotors = ttk.Frame(parent)
        self.unselected_rotors.grid()
        self.rotor_buttons = []

        self.selected_rotors = []
        self.selected_reflector = None

        self.ring_setting_str = StringVar()
        self.initial_pos_str = StringVar()
        self.plugboard_str = StringVar()

        self.final_settings = {}

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
        b = 'B'
        self.reflector_b = ttk.Button(self.unselected_rotors, text=b, command= lambda: self.reflector_click(b)).grid(column=4, row=1)
        c = 'C'
        self.reflector_c = ttk.Button(self.unselected_rotors, text=c, command=lambda: self.reflector_click(c)).grid(column=5, row=1)

        self.ring_setting_text = ttk.Label(self.unselected_rotors, text='Ring Setting').grid(column=6, row=0)
        self.ring_setting = ttk.Entry(self.unselected_rotors, textvariable=self.ring_setting_str).grid(column=6, row=1)

        self.initial_setting_text = ttk.Label(self.unselected_rotors, text='Initial Position').grid(column=6, row=2)
        self.initial_setting = ttk.Entry(self.unselected_rotors, textvariable=self.initial_pos_str).grid(column=6, row=3)

        self.plugboard_text = ttk.Label(self.unselected_rotors, text='Plugboard').grid(column=0, row=4, columnspan=6)
        self.plugboard = ttk.Entry(self.unselected_rotors, width=40, textvariable=self.plugboard_str).grid(column=0, row=5, columnspan=5)

        self.start_btn = ttk.Button(self.unselected_rotors, text='Start', command=lambda: self.start()).grid(column=6, row=4, columnspan=2)


    def reflector_click(self, refl):
        self.selected_reflector = refl
        print(self.selected_reflector)

    def rotor_click(self, i):
        self.selected_rotors.append(self.rotor_buttons[i]['text'])
        print(self.selected_rotors)

    def start(self):
        print(self.ring_setting_str.get())
        print(self.initial_pos_str.get())
        print(self.plugboard_str.get())
        self.final_settings['rotors'] = self.selected_rotors
        self.final_settings['reflector'] = self.selected_reflector
        self.final_settings['ring_setting'] = self.ring_setting_str.get()
        self.final_settings['initial_position'] = self.initial_pos_str.get()
        self.final_settings['plugboard'] = self.plugboard_str.get()

        settings_file = open('settings.json', 'w')
        json.dump(self.final_settings, settings_file)
        settings_file.close()

if __name__ == "__main__":
    root = Tk()
    Menu(root)
    root.mainloop()


def destroy_btn(btn):
    btn.grid_forget()
