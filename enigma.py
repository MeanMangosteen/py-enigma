#!/usr/bin/python3

# simple text to rotor conersion

import json

enigma = {}  # this is the machine


def setup():
    rotors_json = open('rotors_v2.json', 'r')
    reflectors_json = open('reflectors_v2.json', 'r')

    rotors = json.load(rotors_json)
    reflectors = json.load(reflectors_json)

    enigma['rotors'] = rotors
    enigma['reflectors'] = reflectors

    set_ring_setting()


# read text from user
# TODO: should take in list of rotor objects not rotor strings
def rotor_encrypt(letter, rotor_list, reverse=False):
    # rightmost rotor is turned before encryption
    turn_rotor(rotor_list[-1])
    # reverse the 'rotor_list', letter goes
    # through last rotor first in forward direction
    if not reverse:
        rotor_list = list(reversed(rotor_list))
    for rotor in rotor_list:
        # get rotor map depending on direction of signal
        if reverse:
            rotor_map = enigma['rotors'][rotor]['wires_reverse']
        else:
            rotor_map = enigma['rotors'][rotor]['wires_forward']
        # update the letter to encrypt for next rotor
        letter = rotor_map[letter]
        print(letter)
    # letter is now e
    return letter


# TODO: takes a list of rotor objects
def turn_rotors(rotor_list):
    last_element = len(rotor_list) - 1
    first_element = 0
    # set all all rotors won't turn
    for rotor in rotor_list:
        rotor['turn'] = False;
    rotor_list[-1]['turn'] = True  # rightmost rotor always turns
    for i in range(last_element, first_element, -1):  # '-1' mean negative step
        current_rotor = rotor_list[i]
        rotor_leftof = rotor_list[i - 1]  # the rotor leftof current rotor
        # turn both current rotor and one to left if in notch position
        if current_rotor['position'] == current_rotor['notch']:
            current_rotor['turn'] = True
            rotor_leftof['turn'] = True

    for rotor in rotor_list:
        if rotor['turn']:
            # turn the rotor letter by one
            rotor['position'] = chr(ord(rotor['position']) + 1)
            # return

# TODO: throw exception if letter not with 'A' and 'Z'
def shift_letter(letter, num_shifts):
    letter = chr(ord(letter) + num_shifts)
    if ord(letter) > ord('Z'):  # wrap back around 'A' if greater than 'Z'
        letter = chr(ord('A') + ord(letter) - ord('Z') - 1)
    elif ord(letter) < ord('A'):  # wrap back around 'Z' if less than 'A'
        letter = chr(ord('Z') + ord(letter) - ord('A') + 1)
    return letter


def set_ring_setting():
    for rotor in enigma['rotors'].keys():
        rotor['setting'] = 'A'
        rotor['position'] = 'A'


# print out converted text from map

if __name__ == "__main__":
    setup()
    a = rotor_encrypt('A', ['III', 'II', 'I'])
    print("now revesring")
    a = rotor_encrypt('T', ['I', 'II', 'III'], reverse=True)
# TODO: with 3 rotors
# TODO: with reflector
# TODO: with inverse encryption
