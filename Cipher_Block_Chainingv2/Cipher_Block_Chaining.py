"""
This is a simplified CBC encoder and decoder, and the first code I've created without a prompt from codewars
Needless to say, it simplifies CBC and does not reflect the complexity of CBC by any means

Seido Karasaki(yakitategohan on github)
v1 2/5/2023
"""
# Uncomment random if you would like to see the random tests
# import random


class CBC:
    def __init__(self, key, IV):
        self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        self.encryption_key = []
        # Change key into a list with base64 indices
        self.decryption_key = []
        self.key = key
        key_index = 0
        for char in key:
            try:
                self.decryption_key.append((self.alphabet.index(char), key_index))
                key_index += 1
            except:
                raise Exception(
                    'Key must contain characters from alphabet. If alphabet is not specified, defaults to base64'
                )
        # Make decryption key
        self.encryption_key = sorted(self.decryption_key)

        # IV must be same length as key
        if len(IV) != len(key):
            raise Exception('IV must be same length as key')
        self.IV = IV

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

        # If there is any text left over, append it to last_block
        last_block = ''
        if binary:
            last_block = binary

        # XOR with IV if it's the first block of code, otherwise IV with previous encrypted block
        for block in blocks:
            if first:
                xor_block = ''
                for x in range(len(block)):
                    xor_block += str(int(block[x]) ^ int(self.IV[x]))
                # Now encrypt it
                encrypted = ''
                for x, y in self.encryption_key:
                    encrypted += xor_block[y]
                result.append(encrypted)
                first = False
            else:
                xor_block = ''
                for x in range(len(block)):
                    xor_block += str(int(block[x]) ^ int(result[-1][x]))
                encrypted = ''
                for x, y in self.encryption_key:
                    encrypted += xor_block[y]
                result.append(encrypted)

        # Check for last block
        if last_block:
            xor_block = ''
            for x in range(len(last_block)):
                xor_block += str(int(last_block[x]) ^ int(result[-1][x]))

            # Make another encryption key, this time w/ indexes only going up to length of last block
            last_block_key = []
            last_block_count = 0
            for char in self.key[:len(last_block)]:
                last_block_key.append((self.alphabet.index(char), last_block_count))
                last_block_count += 1
            encrypted = ''
            for x, y in sorted(last_block_key):
                encrypted += xor_block[y]
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

        # Check for last block
        last_block = ''
        if binary:
            last_block = binary

        # Decrypt each block, then XOR. First block will be XOR'd by IV, other blocks by ciphertext
        result = []
        first = True
        count = 0
        for block in blocks:
            decrypted_block = ''
            # Decrypt
            decrypt_counter = 0
            while decrypt_counter < len(block):
                spot = 0
                for x, y in self.encryption_key:
                    if y == decrypt_counter:
                        decrypted_block += block[spot]
                        break
                    spot += 1
                decrypt_counter += 1
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

        # Check for last block
        if last_block:
            # Decrypt it
            decrypted_block = ''
            last_block_key = []
            last_block_count = 0
            for char in self.key[:len(last_block)]:
                last_block_key.append((self.alphabet.index(char), last_block_count))
                last_block_count += 1
            decrypt_counter = 0
            while decrypt_counter < len(last_block):
                spot = 0
                for x, y in sorted(last_block_key):
                    if y == decrypt_counter:
                        decrypted_block += last_block[spot]
                        break
                    spot += 1
                decrypt_counter += 1
            # XOR it
            de_xor = ''
            for x in range(len(last_block)):
                de_xor += str(int(decrypted_block[x]) ^ int(blocks[-1][x]))
            result.append(de_xor)
        # Change back to base64
        decrypted_binary = ''.join(result)
        decrypted_text = ''
        while decrypted_binary:
            decrypted_text += self.alphabet[int(decrypted_binary[:6], 2)]
            decrypted_binary = decrypted_binary[6:]
        return decrypted_text


"""
Some Random Tests to prove the code works.

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
print(len(test.to_binary('thisiSaLengtHTest')))
print(test.encode('wLlithIswork'))
print(test.decode('MvZ/o9neFh+H'))
test4 = CBC('UNeVenpaSsWord', '10100110101001')
print(test4.encode('theUltimateTESTTTT'))
print(test4.decode('WCDfCQnDqLyjZjeGsM'))
print(test4.encode('WhyIsnthTHISWroking'))
print(test4.decode('+evaW8AHaM3yWvW2dMT'))
print(test4.encode('anoTherTESTT'))
print(test4.decode('4u4Nb+5eRNTE'))

random_text = 'xlkzjsldflALKSJDKX012857ojflakjdfljLKMKXNCIORkljkdfjsiweruoffmlasf8ruowjklsdsjdfa129038uosfajshfna8'
print(len(random_text))
random_key = ''.join(random.sample('absdfjojcfLKSFJmxc0123456789',28))
random_IV = ''
for x in range(len(random_key)):
    random_IV += str(random.randint(0,1))
randomCBC = CBC(random_key,random_IV)
for x in range(32):
    rand = random_text * random.randint(1,30)
    rand_text =''.join(random.sample(rand,len(rand)))
    rand_encode = randomCBC.encode(rand_text)
    rand_decode = randomCBC.decode(rand_encode)
    print(rand_decode == rand_text)
"""
