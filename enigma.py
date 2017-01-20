#!/usr/bin/python3

# simple text to rotor conersion

import json
import string
import argparse

# TODO: delete selected rotors, this should be determined by args
selected_rotors = ['I', 'II', 'III']
enigma = {}  # this is the machine
# TODO: rotors argument
# TODO: ring setting argument
# TODO: initial position argument
# TODO: reflector argument
# TODO: plug board argument

def setup():
    rotors_json = open('rotors_v2.json', 'r')
    reflectors_json = open('reflectors_v2.json', 'r')

    rotors = json.load(rotors_json)
    reflectors = json.load(reflectors_json)

    # TODO: store selected rotors in a list in 'enigma'
    enigma['all_rotors'] = rotors
    enigma['reflectors'] = reflectors
    enigma['rotors'] = []
    for rotor in selected_rotors:
        enigma['rotors'].append(enigma['all_rotors'][rotor])

    enigma['plugboard'] = ''

    set_ring_setting()


# read text from user
# TODO: should take in list of rotor objects not rotor strings
def rotor_encrypt(letter, rotor_list, reverse=False):

    # reverse the 'rotor_list', letter goes
    # through last rotor first in forward direction
    if not reverse:
        rotor_list = list(reversed(rotor_list))
    for rotor in rotor_list:
        # get rotor map depending on direction of signal
        if reverse:
            rotor_map = rotor['wires_reverse']
        else:
            rotor_map = rotor['wires_forward']
        # update the letter to encrypt for next rotor
        print("letter before: " + letter)
        letter = rotor_map[letter]
        print("letter after: " + letter)
    # letter is now e
    return letter


# TODO: takes a list of rotor objects

def turn_rotors(rotor_list):
    last_element = len(rotor_list) - 1
    first_element = 0

    # initialise by setting all rotors not to turn
    # except rightmost rotor, this always turns
    for rotor in rotor_list:
        rotor['turn'] = False;
    rotor_list[-1]['turn'] = True  # rightmost rotor always turns
    # mark rotors which need to be turned

    for i in range(last_element, first_element, -1):  # '-1' mean negative step
        current_rotor = rotor_list[i]
        rotor_leftof = rotor_list[i - 1]  # the rotor leftof current rotor
        # turn both current rotor and one to left if in notch position
        if current_rotor['position'] == current_rotor['notch']:
            current_rotor['turn'] = True
            rotor_leftof['turn'] = True

    # turn the marked rotors
    for rotor in rotor_list:
        if 'turn' in rotor and rotor['turn']:
            print('we are turning a rotor')
            # turn the rotor letter by one
            rotor['position'] = shift_letter(rotor['position'], 1)


    # TODO: delete, below is for debugging purposes
    print ("Rotor settings are:")
    for rotor in rotor_list:
        print(rotor['position'] + " ", end='')
    print()


# TODO: throw exception if letter not with 'A' and 'Z'
def shift_letter(letter, num_shifts):
    # cleaning num_shifts
    num_shifts = num_shifts % len(string.ascii_uppercase)
    letter = chr(ord(letter) + num_shifts)
    if ord(letter) > ord('Z'):  # wrap back around 'A' if greater than 'Z'
        letter = chr(ord('A') + ord(letter) - ord('Z') - 1)
    elif ord(letter) < ord('A'):  # wrap back around 'Z' if less than 'A'
        letter = chr(ord('Z') + ord(letter) - ord('A') + 1)
    return letter


def get_offsets(rotor):
    positional_offset = ord(rotor['position']) - ord('A')
    setting_offset = ord(rotor['setting']) - ord('A')
    return positional_offset, setting_offset

def set_ring_setting():
    for rotor in enigma['rotors']:
        rotor['setting'] = 'A'
        rotor['position'] = 'A'


# print out converted text from map

if __name__ == "__main__":
    setup()
    turn_rotors(enigma['rotors'])
    a = rotor_encrypt('A', list(reversed(enigma['rotors'])))
    print("now revesring")
    a = rotor_encrypt('T', enigma['rotors'], reverse=True)
# TODO: with 3 rotors
# TODO: with reflector
# TODO: with inverse encryption
