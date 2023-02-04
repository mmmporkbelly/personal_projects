"""
A Vignere Cipher cracker. Currently only works with alphabet letters and on long texts (large sample size needed)
Determine all possible key lengths with Determine_Key_Length, and enter each possible one in get_keyword

Seido Karasaki(yakitategohan on github)
v1 2/3/2023
"""


def get_keyword(ciphertext, key_len):

    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sorted_by_index = []

    # split each character by key_len index
    for index in range(key_len):

        # Temporary string to be added to sorted_by_index
        temp = ''
        while index < len(ciphertext):
            temp += ciphertext[index]
            index += key_len
        sorted_by_index.append(temp)

    # Find the best frequency score for each segment
    key = []
    for subset in sorted_by_index:
        score = 0

        # Check every frequency in alphabet
        for num in range(26):

            # Store freq score
            freq = freq_score(index_shifter(subset, num))

            # If highest frequency score so far, store it
            if freq > score:
                score = freq
                shift = num

        # Take highest stored frequency score, note the shift, and add the letter to the resulting key
        key.append(alpha[(26 - shift) % 26])
    return ''.join(key)

def freq_score(text):
    freqs = {
        'E': 11.1607,
        'A': 8.4966,
        'R': 7.5809,
        'I': 7.5448,
        'O': 7.1635,
        'T': 6.9509,
        'N': 6.6544,
        'S': 5.7351,
        'L': 5.4893,
        'C': 4.5388,
        'U': 3.6308,
        'D': 3.3844,
        'P': 3.1671,
        'M': 3.0129,
        'H': 3.0034,
        'G': 2.4705,
        'B': 2.0720,
        'F': 1.8121,
        'Y': 1.7779,
        'W': 1.2899,
        'K': 1.1016,
        'V': 1.0074,
        'X': 0.2902,
        'Z': 0.2722,
        'J': 0.1965,
        'Q': 0.1962
    }

    score = 0
    for c in text:
        if c in freqs:
            score += freqs[c.upper()]
    return score

def index_shifter(text, shift):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = ''
    for char in text:
        if char in alpha:
            res += alpha[(alpha.index(char) + shift) % 26]
        else:
            res += char
    return res

"""

    Some of my old code- I first just tried by assuming the most frequent character would = 'e'
    Needless to say, it did not work...
    
    This following section was part of my first version of get_keyword.
    
    # Get most likely letters of letter e in each string in list
    letter_e = []
    for string in sorted_by_index:
        letter_e.append(frequency_analysis(string))

    # See how far each letter is from string, append that to list
    key = []
    index_e = alpha.index('E')
    for char in letter_e:
        key.append(alpha[alpha.index(char)-alpha.index('E')])


This function was used to find the letter that occured the most

# Return the letter that occurs the most. Most likely to be the letter 'E'
def frequency_analysis(string):
    # Set variables
    number_of_occurences = 0
    for char in string:
        if string.count(char) > number_of_occurences:
            number_of_occurences = string.count(char)
            letter_e = char
    return letter_e
"""
