#!/usr/bin/python3

# simple text to rotor conersion

import json
import string
from collections import namedtuple

Rotor = namedtuple('Rotor', ['wires_forward', 'wires_backward', 'notch'])
enigma = {}  # this is the machine


def setup():
    rotors_json = open('rotors_v2.json', 'r')
    reflectors_json = open('reflectors_v2.json', 'r')

    rotors = json.load(rotors_json)
    reflectors = json.load(reflectors_json)

    enigma['rotors'] = rotors
    enigma['reflectors'] = reflectors


# read text from user
# print out converted text from map

if __name__ == "__main__":
    setup()
# TODO: with 3 rotors
# TODO: with reflector
# TODO: with inverse encryption
