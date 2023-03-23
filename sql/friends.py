import sqlite3

conn = sqlite3.connect("friends.db")
c = conn.cursor()

# CREATE TABLE
# c.execute("CREATE TABLE friends
# (first_name TEXT, last_name TEXT, closeness INTEGER);")

# BAD DON'T ENTER THIS WAY
# form_first = "Dana"
# query = f"INSERT INTO friends (first_name) VALUES ('{form_first}')"
# c.execute(query)

# BETTER WAY
# data = ("Steve", "Irwin", 9)
# query = "INSERT INTO friends (first_name, last_name, closeness)
# VALUES (?,?,?)"

# BULK INSERTS
query = "INSERT INTO friends VALUES (?,?,?)"
people = [
    ("Roald", "Dahl", 7),
    ("Louise", "Erdrich", 8),
    ("Jacques", "Rutsky", 10),
    ("John", "Cavanaugh", 8),
    ("Eddie", "Chan", 9),
    ("Leo", "Eylar", 8),
]
# WAY ONE
# c.executemany(query, people)

# WAY TWO, lets you edit data along the way
# for person in people:
#     c.execute(query, person)
#     print(person)

# BULK SELECTING

c.execute("SELECT * FROM friends")
# WAY ONE
# for result in c:
#     print(result)

# WAY TWO
# print(c.fetchall())

# print(c.fetchall())


conn.commit()
conn.close()
