"""
Database Project
Written by: Alexander Fitzsimmons, Jabari Gilliss, Jeff Morrow, Seido Karasaki
Cohort: ntl01-cyen-live-010923
Description: A database project to store, edit, write, and read student grades
"""

student_db = {
    'Alex': {'CRY': 'A', 'PYT': 'A', 'GRC': 'A'},
    'Jabari': {'CRY': 'A', 'PYT': 'A', 'GRC': 'A'},
    'Jeff': {'CRY': 'A', 'PYT': 'A', 'GRC': 'A'},
    'Seido': {'CRY': 'A', 'PYT': 'A', 'GRC': 'A'}
}  # {student:{course:grade}}
filename = "data.txt"
course_list = []


def read_data(file):
    try:
        fh = open(filename, "r")
        file = fh.read()
        file = [f for f in file.split('\n') if f != ""]
    except FileNotFoundError:
        print("File not found")

    except Exception as err:
        print("Error {}".format(err))
    else:
        for line in file:
            stu, courses = line.split("|")
            student_db[stu] = {}  # Sets the value as an empty dictionary
            courses = courses.strip("\n")  # Removes the line feed
            courses = courses.strip(",")  # Removes the comma at the end of the line
            for coursepair in courses.split(","):
                (co, gr) = coursepair.split(":")
                student_db[stu][co] = gr
                if co not in course_list:  # Maintain a list of all courses
                    course_list.append(co)
        fh.close()


def write_data(file):
    f = open(filename, 'w')
    for students, courses in student_db.items():
        f.write(students + "|")
        for course, grade in courses.items():
            f.write(course + ": " + str(grade) + ",")
        f.write("\n")
    f.close()


def add_student():
    # Check if student is in dictionary
    student = input('What is the name of the student you want to add?\n')
    if student in student_db.keys():
        raise ('Error: Student already exists in database!')

    # Check if student name is alphabet or not
    elif not student.isalpha():
        raise ('Error, student name must only contain alphabet.')

    # Get courses
    course_num = input(
        'Enter how many courses you would like to add\n'
    )
    courses = {}
    for x in range(int(course_num)):
        course = input('What is the name of the course you would like to add?\n')
        if course not in course_list:
            course_list.append(course)
        while True:
            grade = input('What is the grade for the student?\n')
            if grade not in 'ABCDFabcdf':
                grade = input('Please enter a valid grade [A,B,C,D,F]\n')
            else:
                break
        courses[course] = grade.upper()

    # Add student if this all checks out
    student_db[student] = courses
    print('Successfully added student')


def add_course():
    student_name = input("What is the name of the student?\n")

    if student_name in student_db.keys():
        student_course = input("What is the course to add?\n")
        if student_course not in course_list:
            course_list.append(student_course)
        student_grade = input("What is the grade to add?\n")
        student_db[student_name][student_course] = student_grade
    else:
        raise ('Student does not exist, please add student first')


def print_report_card():
    print("*** Report cards")
    for stu in student_db.keys():
        print("\n\t{}'s Report Card:".format(stu))
        for (course, grade) in student_db[stu].items():
            print("\t{:10}\t{}".format(course, grade))


def print_classes():
    print("*** Classes")
    course_list.sort()
    for courses in course_list:
        print("\n{}:".format(courses))
        for stu in student_db:
            if courses in student_db[stu].keys():
                print("\t{:15}\t{}".format(stu, student_db[stu][courses]))


def print_menu():
    print("\n1. Add a student")
    print("2. Add a course and grade")
    print("3. Print all report cards")
    print("4. Print classes and grades")
    print("5. Read data")
    print("6. Save data")
    print("7. Exit")


if __name__ == "__main__":

    choice = 0
    while True:
        print_menu()
        try:
            choice = int(input("Please select a menu item [1-7]: "))
        except Exception as err:
            print("Please select from the menu!")
        else:
            if choice == 1:
                add_student()
            elif choice == 2:
                add_course()
            elif choice == 3:
                print_report_card()
            elif choice == 4:
                print_classes()
            elif choice == 5:
                read_data(filename)
            elif choice == 6:
                write_data(filename)
            elif choice == 7:
                print('Thank you for using our program!')
                quit()
            else:
                print("That isn't one of the choices. Please select from the menu!!")
                print("Thank you!")
