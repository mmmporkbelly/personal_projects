"""
A Vignere encoder and decoder implemented in Python 3

Includes the flexibility to enter your own alphabet and your own key
NOTE: This is a program to create ciphers and decode ciphers that you have created in the program
This is not a program for brute force decoding of Vignere ciphers

Seido Karasaki (yakitategohan on GitHub)
v1 1/23/2023
"""


class VigenereCipher(object):
    # Instantiate key and alphabet to cycle through. Default is alphanumeric unless specified otherwise
    default = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    def __init__(self, key, alphabet=default):
        self.key = key
        self.alphabet = alphabet

    def encode(self, text):
        result = ''
        alpha_length = len(self.alphabet)
        key_place = 0

        # Iterate through text
        for char in text:

            # Shuffle key IF character is in defined alphabet
            if char in self.alphabet:
                if key_place == len(self.key):
                    key_place = 0
                key_ind = self.alphabet.index(self.key[key_place])
                ind = (self.alphabet.index(char) + key_ind) % alpha_length
                result += self.alphabet[ind]
                key_place += 1

            # If not in defined alphabet, do not shuffle, leave as is
            else:
                if key_place == len(self.key):
                    key_place = 0
                result += char
                key_place += 1
        return result

    def decode(self, text):
        result = ''
        alpha_length = len(self.alphabet)
        key_place = 0

        # Iterate through text
        for char in text:

            # Decode if char is in defined alphabet
            if char in self.alphabet:
                if key_place == len(self.key):
                    key_place = 0
                key_ind = self.alphabet.index(self.key[key_place])
                ind = (self.alphabet.index(char) - key_ind) % alpha_length
                result += self.alphabet[ind]
                key_place += 1
            else:
                if key_place == len(self.key):
                    key_place = 0
                result += char
                key_place += 1
        return result


if __name__ == "__main__":

    # Instantiate the cipher obj IF running file as main
    alphabet = input(
        'Welcome to the Vignere Cipher encoder and decoder. Please enter the alphabet that you would like to use.\n'
        'If you would like to use the default of an alphanumeric alphabet, please simply press enter.\n'
    )
    key = input(
        'What key would you like to use? Please note that every letter in the key must be within the \n'
        'specified alphabet. I.e., if using the default alphabet, key must be alphanumeric for this code to work.\n'
    )

    # Use default alphabet unless otherwise specified
    if alphabet == '':
        instance = VigenereCipher(key)
    else:
        instance = VigenereCipher(key, alphabet=alphabet)

    # Let user decode and encode until they mention that they would like to quit
    while True:
        action = input(
            'Would you like to encode or decode? Type quit to quit.\n'
        )
        if action[0].lower() == 'q':
            quit()

        # Make sure they type encode or decode
        while action[0].lower() != 'e' and action[0].lower() != 'd':
            action = input('Please input encode or decode \n')

        # If encode
        if action[0].lower() == 'e':
            text = input('What would you like to encode? \n')
            print(f'Here is the encoded text: \n {instance.encode(text)}')

        # If decode
        else:
            text = input('What would you like to decode? \n')
            print(f'Here is the decoded text: \n {instance.decode(text)}')
