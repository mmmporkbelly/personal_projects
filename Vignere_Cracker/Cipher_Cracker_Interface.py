"""
A user friendly interface to decode a Vignere Cipher.
Imports code from Cipher_Cracker and Determine_Key_Length. Only works on Vignere Ciphers written with the alphabet
Also included my decoder from Vigner_Cipher_Decoder_and_Encoder

Seido Karasaki(yakitategohan on github)
v1 2/3/2023
"""

import Cipher_Cracker
import Determine_Key_Length


# From Vignere_Cipher_Decoder_and_Encoder, sle5ightly edited
def decode(text, key):
    result = ''
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alpha_length = len(alphabet)
    key_place = 0

    # Iterate through text
    for char in text:

        # Decode if char is in defined alphabet
        if char in alphabet:
            if key_place == len(key):
                key_place = 0
            key_ind = alphabet.index(key[key_place])
            ind = (alphabet.index(char) - key_ind) % alpha_length
            result += alphabet[ind]
            key_place += 1
        else:
            if key_place == len(key):
                key_place = 0
            result += char
            key_place += 1
    return result


if __name__ == '__main__':
    # Offer direct input or text file option
    action = input(
        'Hello, welcome to the Vignere Code Cracker.\n'
        'Would you like to input text directly, or would you like to load a code file? [d/i]\n'
    )
    while action[0].lower() != 'd' and action[0].lower() != 'i':
        action = input('Please indicate whether you would like to [d]irectly input or [i]nput a file name\n')
    action = action[0].lower()

    # If direct input
    if action == 'd':
        text_with_other_characters = input('Please enter the text you would like to decode\n')
        # Make sure text has only alphabet characters
        text = ''
        for char in text_with_other_characters:
            if char.isalpha():
                text += char
        possible_lengths = Determine_Key_Length.all_possible_key_lengths(text)
        print(f'Here are the possible key lengths:\n{possible_lengths}')
        input('Press enter to continue\n')
        possible_keys = []
        for num in possible_lengths:
            possible_keys.append(Cipher_Cracker.get_keyword(text, num))
        print(f'Here are the possible keys:\n{possible_keys}')
        input('Press enter to continue\n')
        for key in possible_keys:
            input(f'Please press enter if you would like to see the cipher text decoded with this key:\n{key}\n')
            print(decode(text, key))
        print('You have tried all possibilities. Thank you for using!')

    else:
        file = input('Please enter the filepath of the text you would like to decode\n')
        while True:
            try:
                with open(file) as f:
                    text_with_other_characters = f.read()
                break
            except:
                file = input('Please enter a valid filepath\n')
        # Make sure text has only alphabet characters
        text = ''
        for char in text_with_other_characters:
            if char.isalpha():
                text += char
        possible_lengths = Determine_Key_Length.all_possible_key_lengths(text)
        print(f'Here are the possible key lengths:\n{possible_lengths}')
        input('Press enter to continue\n')
        possible_keys = []
        for num in possible_lengths:
            possible_keys.append(Cipher_Cracker.get_keyword(text, num))
        print(f'Here are the possible keys:\n{possible_keys}')
        input('Press enter to continue\n')
        for key in possible_keys:
            input(f'Please press enter if you would like to see the cipher text decoded with this key:\n{key}\n')
            print(decode(text, key))
        print('You have tried all possibilities. Thank you for using!')
