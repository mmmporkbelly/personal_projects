"""
This is a simplified CBC encoder and decoder, and the first code I've created without a prompt from codewars
Needless to say, it simplifies CBC and does not reflect the complexity of CBC by any means

Seido Karasaki(yakitategohan on github)
v1 2/5/2023
"""


class CBC:
    def __init__(self, key, IV):
        self.key = key
        self.IV = IV
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

    def to_binary(self, text):
        binary = ''
        for char in text:
            binary += f'{self.alphabet.index(char):06b}'
        return binary

    def encode(self, text):
        blocks = []
        # Change text to binary based on index of character in base64 alphabet
        binary = ''
        for char in text:
            binary += f'{self.alphabet.index(char):06b}'

        # Split binary text into blocks of code by key length
        while len(binary) >= len(self.key):
            blocks.append(binary[:len(self.key)])
            binary = binary[len(self.key):]
        first = True
        result = []

        # XOR with IV if it's the first block of code, otherwise IV with previous encrypted block
        for block in blocks:
            if first:
                xor_block = ''
                for x in range(len(block)):
                    xor_block += str(int(block[x]) ^ int(self.IV[x]))
                # Now encrypt it
                encrypted = ''
                zipped = zip(self.key, xor_block)
                for x in sorted(zipped):
                    encrypted += x[1]
                result.append(encrypted)
                first = False
            else:
                xor_block = ''
                for x in range(len(block)):
                    xor_block += str(int(block[x]) ^ int(result[-1][x]))
                encrypted = ''
                zipped = zip(self.key, xor_block)
                for x in sorted(zipped):
                    encrypted += x[1]
                result.append(encrypted)

        # Now change back to base64
        cipher_binary = ''.join(result)
        encrypted_text = ''
        while cipher_binary:
            encrypted_text += self.alphabet[int(cipher_binary[:6], 2)]
            cipher_binary = cipher_binary[6:]
        return encrypted_text

    def decode(self, text):
        binary = ''
        # Change to binary
        for char in text:
            binary += f'{self.alphabet.index(char):06b}'

        # Separate into blocks
        blocks = []
        while len(binary) >= len(self.key):
            blocks.append(binary[:len(self.key)])
            binary = binary[len(self.key):]

        # Decrypt each block, then XOR. First block will be XOR'd by IV, other blocks by ciphertext
        result = []
        first = True
        count = 0
        for block in blocks:
            decrypted_block = ''
            # Decrypt
            for x in self.key:
                decrypted_block += block[int(x)]
            # Now XOR it
            if first:
                de_xor = ''
                for x in range(len(block)):
                    de_xor += str(int(decrypted_block[x]) ^ int(self.IV[x]))
                result.append(de_xor)
                first = False
            else:
                de_xor = ''
                for x in range(len(block)):
                    de_xor += str(int(decrypted_block[x]) ^ int(blocks[count][x]))
                result.append(de_xor)
                count += 1

        # Change back to base64
        decrypted_binary = ''.join(result)
        decrypted_text = ''
        while decrypted_binary:
            decrypted_text += self.alphabet[int(decrypted_binary[:6], 2)]
            decrypted_binary = decrypted_binary[6:]
        return decrypted_text


test = CBC('4321590867', '1010010100')
test1 = CBC('4752613098', '0010011010')
test2 = CBC('2319708564', '1011000011')
test3 = CBC('6384570219', '1101110110')
print(test.encode('ThiSisMyVerYFirStKataEver'))
print(test.decode('vLffvlKrX92zeXpYglI1OPCyQ'))
print(test1.encode('CodingCanbeSoOOOfunNnnnnn'))
print(test1.decode('RizTpPpMDb0+32GI7LC6LObh2'))
print(test2.encode('ThisisAmucHlongerTestDontfailItOrElSEYouCANTpasSSs'))
print(test2.decode('+8tf4kbkw6ClakKQUgz+J61rusIAxr4YThvFuJgCAyJm7gAow6'))
print(test3.encode('ThiSWillBeTheUltimATECHALLENGEwillYouPassorWillYOUFAIlLetUSseeTheResultTThAhAHAh'))
print(test3.decode('6gGeD1Jqj2+LD8YGLPrZg9BfAH2ITbW+f3ZWwbQrDthiQivaa3buR7IVmAKav1F5hfz6KhLXf/duPv/O'))
