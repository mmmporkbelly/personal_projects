"""
Made to take attendance for Flatiron Zoom
Use by running file + destination. Example:
./attendance.py -f /home/__username__/downloads/example.csv
Seido Karasaki(yakitategohan on github)
v1 2/27/2023
"""
import csv
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_location", dest='location', help='File location')
    options = parser.parse_args()
    return options


def get_students(file_name):
    # List of students:
    student_list = [
        'Alex Cantin',
        'Alexander Fitzsimmons',
        'Blake Robinson',
        'Brittany Magness',
        'Cherisee Allick',
        'Connie Hua',
        'Daniel Soto',
        'Jabari Gillis',
        'Jacob Carlson',
        'Jeff',
        'Jeremiah Guliuzza',
        'Jeremy F',
        'Kevin Deppe',
        'Leotrim Kelmendi',
        'Mark Hallowell',
        'Marquis Crawford',
        'Rowen Windemuller',
        'shalanda moore',
        'Stephen Campion',
        'Thomas Gallo',
        "Tom O'Donnell",
        'Touly Moua',
        'Trey Mooneyham',
        'Tuie Pham',
        'Vivian Hua'
    ]
    # Attendance List
    attendance = []
    with open(file_name) as meeting_data:
        # Grabs student info
        reader = csv.reader(meeting_data)
        for student_info in reader:
            name = student_info[0]
            user_id = student_info[1]
            if name in student_list:
                student_list.pop(name)
            elif user_id in student_list:
                student_list.pop(user_id)
            attendance.append(name)
        meeting_data.close()

    print(f'[+]\t Who is present: {attendance}\n[+]\t Who is not: {student_list}')


if __name__ == "__main__":
    file_location = get_arguments().location
    get_students(file_location)
