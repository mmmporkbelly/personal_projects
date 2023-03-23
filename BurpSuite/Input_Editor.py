"""
Edit username and password lists to whatever function you want
Seido Karasaki(yakitategohan on github)
v1 02/20/2023
"""


# When you want to enumerate over the same item a couple of times but BurpSuite won't do it for you
def repeat_each_item(file, number, output):
    try:
        fh = open(file, 'r')
        text = fh.read()
        text = [f for f in text.split('\n') if f != ""]
    except FileNotFoundError:
        print("File not found")
        quit()
    # Now rewrite file and repeat each line in text to the times specified
    new_text = ''
    for value in text:
        for x in range(int(number)):
            new_text += f'{value}\n'
    result = open(output, 'w')
    result.write(new_text)
    result.close()
    fh.close()
    print(f'Each value in your original file has now been written {number} number of times in the file name: '
          f'{output}')


def add_after_every_line(file, number, insert, output):
    try:
        fh = open(file, 'r')
        text = fh.read()
        text = [f for f in text.split('\n') if f != ""]
    except FileNotFoundError:
        print("File not found")
        quit()
    # Now rewrite file and repeat value every x number of lines
    new_text = ''
    counter = 1
    for value in text:
        new_text += f'{value}\n'
        if counter == int(number):
            new_text += f'{insert}\n'
            counter = 0
        counter += 1
    result = open(output, 'w')
    result.write(new_text)
    result.close
    fh.close()
    print(f'The value of {insert} has now been written every {number} times in addition to the original text in the'
          f' following file: {output}')


def to_json_list(file, output):
    try:
        fh = open(file, 'r')
        text = fh.read()
        text = [f for f in text.split('\n') if f != ""]
    except FileNotFoundError:
        print("File not found")
        quit()
    # Now simply rewrite to json format
    new_text = '[\n'
    for value in text:
        new_text += f'\t"{value}",\n'
    new_text += ']'
    result = open(output, 'w')
    result.write(new_text)
    result.close
    fh.close()
    print(f'You have successfully written your list in json format to this location: {output}')


if __name__ == '__main__':
    print('Welcome to a simple text editor. This will help edit your user/pw files to help exploit vulnerabilities '
          'easier.')
    possible_commands = {
        0: 'Repeat each item: repeat each item in list consecutively x number of times. Useful to see'
           ' what server response is to failed login attempts on BurpSuite.',
        1: 'Add a single item after x number of rows: Userful for any APIs that lockout after x amount of times. '
           'Useful to reset lockout attempts by juxtaposing with successful lockout attempts.',
        2: 'Change to json: If username/pw input in POST request is in json format, attacker can sometimes post a '
           'list in the password field. This function will change your original text to a list and save it in a file.'
    }
    # Get input and output file names
    file_name = input('What file would you like to open?\n')
    output_name = input('What would you like the resulting file to be called?\n')

    # Give choices for commands
    print(f'What command would you like to execute? Here are the possible commands:')
    for x, y in possible_commands.items():
        print(f'{x} : {y}')
    command = input(f'Please type a number:\n')
    if command == '0':
        number = input('You have selected to repeat each item in a list. How many times would you like to repeat '
                       'each item?\n')
        repeat_each_item(file_name, number, output_name)
    elif command == '1':
        insert = input('You have selected to insert a value into a list every x number of times. What would you'
                       ' like to insert?\n')
        number = input('How often would like to repeat this input? Enter a number\n')
        add_after_every_line(file_name, number, insert, output_name)
    elif command == '2':
        to_json_list(file_name, output_name)
