#!/usr/bin/python3

# simple text to rotor conersion

import json
import string

enigma = {}  # this is the machine
# TODO: rotors argument
# TODO: ring setting argument
# TODO: initial position argument
# TODO: reflector argument
# TODO: plug board argument

def setup():
    # opening file stuff
    rotors_json = open('rotors_v2.json', 'r')
    reflectors_json = open('reflectors_v2.json', 'r')
    settings_json = open('settings.json', 'r')

    # loading json from file stuff
    rotors = json.load(rotors_json)
    reflectors = json.load(reflectors_json)
    settings = json.load(settings_json)

    # populate info on all rotors and reflectors avail stuff
    enigma['all_rotors'] = rotors
    enigma['all_reflectors'] = reflectors
    enigma['rotors'] = []

    # rotor stuff -- loading selected rotors into machine
    for rotor in settings['rotors']:
        enigma['rotors'].append(enigma['all_rotors'][rotor])

    # reflector stuff
    selected_reflector = settings['reflector']
    enigma['reflector'] = enigma['all_reflectors'][selected_reflector]

    # plugboard stuff
    enigma['plugboard'] = {}

    # populating plugboard
    for i in range(0, len(settings['plugboard']), 2):
        letter_left = settings['plugboard'][i]
        letter_right = settings['plugboard'][i+1]
        enigma['plugboard'][letter_left] = letter_right
        enigma['plugboard'][letter_right] = letter_left

    # settings initial pos and ring setting stuff
    for rotor, ring_letter, pos_letter\
            in zip(enigma['rotors'], settings['ring_setting'], settings['initial_position']):
        rotor['setting'] = ring_letter
        rotor['position'] = pos_letter


def rotor_encrypt(letter, rotor_list, reverse=False):
    # reverse the 'rotor_list', letter goes
    # through last rotor first in forward direction
    if not reverse:
        rotor_list = list(reversed(rotor_list))
    for rotor in rotor_list:
        # positional and setting offsets
        pos_offset, setting_offset = get_offsets(rotor)
        # setting the letter to be the letter which the signal enters
        wiring_offset = pos_offset - setting_offset
        print("the wiring offset is: " + str(wiring_offset))
        letter = shift_letter(letter, wiring_offset)

        # get rotor map depending on direction of signal
        if reverse:
            rotor_map = rotor['wires_reverse']
        else:
            rotor_map = rotor['wires_forward']
        # update the letter to encrypt for next rotor
        print("letter before: " + letter)
        letter = rotor_map[letter]
        letter = shift_letter(letter, setting_offset)
        ring_offset = 26 - pos_offset
        letter = shift_letter(letter, ring_offset)
        print("letter after: " + letter)
    # letter is now e
    return letter


def turn_rotors(rotor_list):
    last_element = len(rotor_list) - 1
    first_element = 0

    # initialise by setting all rotors not to turn
    # except rightmost rotor, this always turns
    for rotor in rotor_list:
        rotor['turn'] = False
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


def reflector(letter):
    return enigma['reflector'][letter]


def plugboard(letter):
    if letter in enigma['plugboard']:
        return enigma['plugboard'][letter]
    else:
        return letter


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


# TODO: make sure all offsets are postive? throw exception
def get_offsets(rotor):
    positional_offset = ord(rotor['position']) - ord('A')
    setting_offset = ord(rotor['setting']) - ord('A')
    print("get_offsets: pos: {}, setting {}".format(positional_offset, setting_offset))
    return positional_offset, setting_offset


if __name__ == "__main__":
    output = ""
    message = input("Enter Text! \n>> ")
    setup()
    for letter in message:
        turn_rotors(enigma['rotors'])
        letter = plugboard(letter)
        letter = rotor_encrypt(letter, enigma['rotors'])
        letter = reflector(letter)
        letter = rotor_encrypt(letter, enigma['rotors'], reverse=True)
        letter = plugboard(letter)
        output += letter
    print("final message: " + output)
