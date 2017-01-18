#!/usr/bin/python3

# simple text to rotor conersion

import json
import string
from collections import namedtuple

Rotor = namedtuple('Rotor', ['wires_forward', 'wires_backward', 'notch'])
enigma = {} # this is the machine

def inverse_dict(original):
    inversed = {}   # inversed dict
    for (key, value) in original.items():
        inversed[value] = key   # reverse key and value
    return inversed

def make_json_file():
    rotors_json = open("reflectors.json", 'r')
    rotors = json.load(rotors_json)

    for rotor_num in rotors.keys():
        # wires forward
        wires_forward = dict(zip(string.ascii_uppercase, list(rotors[rotor_num]['wires'])))
        wires_reverse = inverse_dict(wires_forward) # inverse the dictionary

        enigma[rotor_num] = {}
        enigma[rotor_num]['wires'] = wires_forward

    new_json = open("reflectors_v2.json", 'w')
    json.dump(enigma, new_json)
    print("done!")



# read text from user
# print out converted text from map

if __name__ == "__main__":
    make_json_file()
    for num in enigma.keys():
        print(num)
#TODO: with 3 rotors
#TODO: with reflector
#TODO: with inverse encryption
