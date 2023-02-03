"""
This simple scraper scrapes every page on quotes.toscrape.com, and creates a guessing game

Seido Karasaki (yakitategohan on GitHub)
v1 11/2/2023
"""

from bs4 import BeautifulSoup
import requests
from random import choice
from time import sleep

base = "https://quotes.toscrape.com"
url = "/page/1"
quotes = []


# Function to make a dictionary for quotes
def makeDict(quote, name, link):
    return {"quote": quote, "name": name, "link": link}


# Function to get further information about author from the link if the user needs additional help
def getBirthAndLocation(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.text, "html.parser")
    birthday = soup.find(class_="author-born-date").get_text()
    location = soup.find(class_="author-born-location").get_text()
    return f"This author was born on {birthday} {location}"


# Gets the Bio from author from separate link if user needs help
def getBio(link):
    request = requests.get(link)
    soup = BeautifulSoup(request.text, "html.parser")
    return soup.find(class_="author-description").get_text()


while url:
    # Make a request to quotes.toscrape
    request = requests.get(f"{base}{url}")
    soup = BeautifulSoup(request.text, "html.parser")
    all_quotes = soup.find_all(class_="quote")

    # Get the quotes
    for one_quote in all_quotes:
        quote = one_quote.find(class_="text").get_text()
        name = one_quote.find(class_="author").get_text()
        link = f'https://quotes.toscrape.com{one_quote.find(class_="author").find_next_sibling()["href"]}'
        quotes.append(makeDict(quote, name, link))

    # Now parse through next pages through recursion
    n = soup.find(class_="next")
    if n:
        url = n.find("a")["href"]
        sleep(2)
    else:
        break

guesses = 4
random_selection = choice(quotes)
guess = ""

# Implementation of the game
while guesses >= 0:
    if guess.lower() != random_selection["name"].lower():
        if guesses == 4:
            print(f"I have a quote for you. Who said this?\n{random_selection['quote']}")
            guess = input()
            guesses -= 1

        # If wrong, grab birthdate and birth location
        elif guesses == 3:
            print(
                f"Nope. You have {guesses} guesses left.\n"
                f"I'll give you a hint:\n"
                f"{getBirthAndLocation(random_selection['link'])}")
            guess = input("Guess again: ")
            guesses -= 1
        # If wrong, give initials
        elif guesses == 2:
            print(f"Nope. You have {guesses} guesses left.\nAnother hint. Their initials are:")
            name = random_selection["name"].split(" ")
            first_initial = name[0][0]
            last_initial = name[len(name) - 1][0]
            print(f"{first_initial}. {last_initial}.\n"
                  f"There are {len(name)} words in their name.")
            guess = input()
            guesses -= 1

        # If wrong, provide bio, replace all names with redacted
        elif guesses == 1:
            print(f"Nope. You have {guesses} guess left.")
            print("A big hint:")
            bio = getBio(random_selection["link"])
            for part in name:
                bio = bio.replace(part, 'REDACTED')
            print(bio)
            guess = input()
            guesses -= 1

        # Womp womp, they lost
        elif guesses == 0:
            print(
                "Too bad. You didn't get it, "
                f"the answer was : {random_selection['name']}. "
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
