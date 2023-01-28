import csv
from bs4 import BeautifulSoup
import requests
from random import choice
from time import sleep

base = "https://quotes.toscrape.com"
url = "/page/1"
quotes = []


def makeDict(quote, name, link):
    return {"quote": quote, "name": name, "link": link}


def getBirthAndLocation(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.text, "html.parser")
    birthday = soup.find(class_="author-born-date").get_text()
    location = soup.find(class_="author-born-location").get_text()
    return f"This author was born on {birthday} {location}"


def getBio(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup.find(class_="author-description").get_text()


while url:
    request = requests.get(f"{base}{url}")
    soup = BeautifulSoup(request.text, "html.parser")
    all_quotes = soup.find_all(class_="quote")
    # get the quotes
    for one_quote in all_quotes:
        quote = one_quote.find(class_="text").get_text()
        name = one_quote.find(class_="author").get_text()
        link = f'https://quotes.toscrape.com{one_quote.find(class_="author").find_next_sibling()["href"]}'
        quotes.append(makeDict(quote, name, link))
    # now parse through next pages through recursion
    n = soup.find(class_="next")
    if n:
        url = n.find("a")["href"]
        sleep(2)
    else:
        break

guesses = 4
random_selection = choice(quotes)
guess = ""

while guesses >= 0:
    if guess != random_selection["name"]:
        if guesses == 4:
            print("I have a quote for you. Who said this?")
            print(random_selection["quote"])
            guess = input()
            guesses -= 1
        elif guesses == 3:
            print(f"Nope. You have {guesses} guesses left.")
            print("I'll give you a hint:")
            print(getBirthAndLocation(random_selection["link"]))
            guess = input("Guess again: ")
            guesses -= 1
        elif guesses == 2:
            print(f"Nope. You have {guesses} guesses left.")
            print("Another hint. Their initials are:")
            name = random_selection["name"].split(" ")
            first_initial = name[0][0]
            last_initial = name[len(name) - 1][0]
            print(f"{first_initial}. {last_initial}.")
            guess = input()
            guesses -= 1
        elif guesses == 1:
            print(f"Nope. You have {guesses} guess left.")
            print("A big hint:")
            bio = getBio(random_selection["link"])
            remove_first = bio.replace(name[0], first_initial)
            remove_last = remove_first.replace(name[len(name) - 1], last_initial)
            print(remove_last)
            guess = input()
            guesses -= 1
        elif guesses == 0:
            print(
                "Too bad. You didn't get it."
                f"The answer was : {random_selection['name']}. "
                "Do you want to try again?"
            )
            reply = input("y/n: ")
            if reply[0] == "n":
                break
            else:
                guesses = 4
                guess = ""
                random_selection = choice(quotes)
    else:
        print("You got it!!! Would you like to play again?")
        reply = input("y/n ")
        if reply[0] == "n":
            break
        else:
            guesses = 4
            guess = ""
            random_selection = choice(quotes)
