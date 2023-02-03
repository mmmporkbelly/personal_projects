"""
Decoding and encoding to base 64 without using the python module
Follows protocol of including padding as '='
Seido Karasaki (yakitategohan on GitHub)
v1 2/2/2023
"""


def to_base_64(string):
    # Define base64
    base_64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    binary = ''

    # Iterate through every character in string, convert ASCII index to binary
    for character in string:
        binary += f'{ord(character):08b}'

    # If length of result is not divisible by 6, add 0s till it is, keep track of padding
    padding = ''
    while len(binary) % 6 != 0:
        binary += '0'
        padding += '='

    # Segment binary into groups of six, convert sets into index of base_64
    result = ''
    while binary != '':
        result += f'{base_64[int(binary[:6], 2)]}'
        binary = binary[6:]

    return result + padding


def from_base_64(string):
    # Define base64
    base_64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    binary = ''

    # Check for padding
    count = string.count('=')
    string = string[:-count]

    # Iterate through every character in string, convert base_64 index to binary
    for character in string:
        binary += f'{base_64.index(character):06b}'

    # If count, then subtract # of 0s from count
    if count != 0:
        binary = binary[:-count]

    # Segment binary into groups of six, convert sets into index of base_64
    result = ''
    while len(binary) > 7:
        result += f'{chr(int(binary[:8], 2))}'
        binary = binary[8:]

    return result


# Simple interface if using the file to decode and encode
if __name__ == '__main__':
    func = input('Hello, would you like to encode or decode? \n')
    while func[0].lower() != 'e' and func[0].lower() != 'd':
        func = input('Please input encode or decode \n')
    if func[0].lower() == 'e':
        text = input('Please indicate what you would like to encode into base64\n')
        print(f'Here is your encoded message!\n{to_base_64(text)}')
    else:
        text = input('Please indicate what you would like to decode from base64\n')
        print(f'Here is your encoded message!\n{from_base_64(text)}')
