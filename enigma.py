#!/usr/bin/python3

# simple text to rotor conersion

import json
import string
from collections import namedtuple

enigma = {}  # this is the machine


def setup():
    rotors_json = open('rotors_v2.json', 'r')
    reflectors_json = open('reflectors_v2.json', 'r')

    rotors = json.load(rotors_json)
    reflectors = json.load(reflectors_json)

    enigma['rotors'] = rotors
    enigma['reflectors'] = reflectors


# read text from user
def rotor_encrypt(letter, rotor_list, reverse=False):
    for rotor in rotor_list:
        if reverse:
            rotor_map = enigma['rotors'][rotor]['wires_reverse']
        else:
            rotor_map = enigma['rotors'][rotor]['wires_forward']
        # update the letter to encrypt for next rotor
        letter = rotor_map[letter]
        print(letter)
    # letter is now e
    return letter


# print out converted text from map

if __name__ == "__main__":
    setup()
    a = rotor_encrypt('A', ['III', 'II', 'I'] )
    print("now revesring")
    a = rotor_encrypt('T', ['I', 'II', 'III'], reverse=True)
# TODO: with 3 rotors
# TODO: with reflector
# TODO: with inverse encryption
