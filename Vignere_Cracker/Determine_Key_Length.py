"""
To crack a Vignere Cipher, you must first parse through the cipher to determine if there are any repeated three letter
sequences. Once you do that, find the greatest common denominator between occurences of the three letter sequences.
The GCD that occurs the most is your most likely key length. This code does this; however, we also provide a max key
length to speed up the process. A second function has been added to give all possible key lengths. The two functions are
essentially identical

Seido Karasaki (yakitategohan on GitHub)
v1 2/3/2023
"""

from math import gcd


def get_key_length(cipher_text, max_key_length):
    # Get every 3 letter combination
    count = 0
    list = {}
    while count + 3 <= len(cipher_text):
        # Store 3 letter combination
        temp_3 = cipher_text[count:count + 3]
        if list.get(temp_3):
            # Add index to existing count
            list[temp_3].append(count)
        else:
            # Initialize val into dict
            list[temp_3] = [count]
        count += 1

    # Find the differences between repeating values, store in list
    repeaters = []
    for repeater in list.values():
        if len(repeater) > 1:
            repeaters.append(repeater[1] - repeater[0])

    # Find common denominator
    denominators = []
    for tracker in range(0, len(repeaters) - 1):
        # Find greatest common denominator, only add if less than given length
        denom = gcd(repeaters[tracker], repeaters[tracker + 1])
        if denom <= max_key_length and denom > 1:
            denominators.append(denom)

    # Find the most common occurence in denominators
    occurences = 0
    for denom in denominators:
        print(denominators.count(denom))
        if denominators.count(denom) > occurences:
            occurences = denominators.count(denom)
            key_length = denom

    return key_length


def all_possible_key_lengths(cipher_text):
    # Get every 3 letter combination
    count = 0
    list = {}
    while count + 3 <= len(cipher_text):
        # Store 3 letter combination
        temp_3 = cipher_text[count:count + 3]
        if list.get(temp_3):
            # Add index to existing count
            list[temp_3].append(count)
        else:
            # Initialize val into dict
            list[temp_3] = [count]
        count += 1

    # Find the differences between repeating values, store in list
    repeaters = []
    for repeater in list.values():
        if len(repeater) > 1:
            repeaters.append(repeater[1] - repeater[0])

    # Find common denominator
    denominators = []
    for tracker in range(0, len(repeaters) - 1):
        denom = gcd(repeaters[tracker], repeaters[tracker + 1])
        denominators.append(denom)

    # Return all denominators, eliminate duplicates, remove anything that doesn't occur more than once
    result = []
    for denom in denominators:
        if denominators.count(denom) > 1:
            result.append(denom)
    return sorted(set(result))
