"""
A Rail Cipher encoder and decoder implemented in Python 3

Includes the flexibility to enter the number of rails to decode and encode
Also includes a brute force option

Seido Karasaki (yakitategohan on GitHub)
v1 2/2/2023
"""

def encode_rail_fence_cipher(string, n):
    # No need to create a rail for the encoding, simply create a list with n number of rows
    count = 0
    string = list(string)
    result = []
    for num in range(n):
        result.append('')

    # Now cycle through the n number of rows, append each character to row in zigzag fashion
    """
    row 1 \    / 
    row 2  \  /  
    row 3   \     

    slash = character
    """

    down = True
    for char in string:
        if count == n - 1:
            down = False
        elif count == 0:
            down = True
        result[count] += char
        if down:
            count += 1
        else:
            count -= 1

    return ''.join(result)


def decode_rail_fence_cipher(string, n):
    # Recreate the 'rail system'
    rail = [['' for val in range(len(string))] for row in range(n)]

    # Mark each letter in the railway with a *
    col, row = 0, 0
    down = True
    for place in range(len(string)):
        if row == 0:
            down = True
        elif row == n - 1:
            down = False
        rail[row][col] = '*'
        col += 1
        if down:
            row += 1
        else:
            row -= 1

    # Pop each letter from cipher into rail
    stringlist = list(string)
    for row in range(n):
        for col in range(len(rail[row])):
            if rail[row][col] == '*':
                rail[row][col] = stringlist.pop(0)

    # Now read the cipher! Reuse code of marking rail with *, replace * with adding to result str
    result = ''
    col, row = 0, 0
    down = True
    for place in range(len(string)):
        if row == 0:
            down = True
        elif row == n - 1:
            down = False
        result += rail[row][col]
        col += 1
        if down:
            row += 1
        else:
            row -= 1

    return result


# If you don't know the number of rails...
def brute_force_decode(text):
    # Brute force and check x number of rails, where x is smaller than length of text
    for x in range(2, len(text)):
        print(decode_rail_fence_cipher(text, x) + '\n')


if __name__ == "__main__":

    # If running as a file, get user's input, loop if improper command
    func = input('Hello, would you like to encode or decode? \n')
    while func[0].lower() != 'e' and func[0].lower() != 'd':
        func = input('Please input encode or decode \n')

    # If encode
    if func[0].lower() == 'e':
        text = input('What would you like to encode? \n')
        rails = input('Please input a number of rails \n')
        # Rails cannot be longer than length of text. Has to be number
        while not rails.isdigit() or int(rails) >= len(text) or int(rails) < 0:
            rails = input('Please enter a valid number that is above 0 and below length of text\n')
        print(f'Here is the encoded text: \n {encode_rail_fence_cipher(text,int(rails))}')

    # If decode
    else:
        text = input('What would you like to decode? \n')
        rails = input('Please input a number of rails, or enter brute if you would like to brute force\n')
        while not rails.isdigit() or int(rails) >= len(text) or int(rails) < 0:
            if rails[0].lower() == 'b':
                break
            else:
                rails = input('Please enter a valid number that is above 0 and below length of text or enter brute')
        # If brute force
        if rails[0].lower() == 'b':
            brute_force_decode(text)
        else:
            print(f'Here is your decoded text: {decode_rail_fence_cipher(text, int(rails))}')
