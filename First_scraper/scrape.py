import csv
from bs4 import BeautifulSoup
import requests
from time import sleep

base = "https://quotes.toscrape.com"


def makeDict(quote, name, link):
    return {"quote": quote, "name": name, "link": link}


def scraper(base):
    url = "/page/1"
    quotes = []
    while url:
        request = requests.get(f"{base}{url}")
        soup = BeautifulSoup(request.text, "html.parser")
        all_quotes = soup.find_all(class_="quote")
        # get the quotes
        for one_quote in all_quotes:
            quote = (
                one_quote.find(class_="text")
                .get_text()
                .replace("'", "")
                .replace('"', "")
            )
            name = one_quote.find(class_="author").get_text()
            link = f'https://quotes.toscrape.com{one_quote.find(class_="author").find_next_sibling()["href"]}'
            quotes.append(makeDict(quote, name, link))
        # now parse through next pages through recursion
        n = soup.find(class_="next")
        if n:
            url = n.find("a")["href"]
            sleep(1)
        else:
            break
    return quotes


with open("quotes.csv", "w") as file:
    write = csv.DictWriter(file, fieldnames=["quote", "name", "link"])
    write.writeheader()
    for row in scraper("https://quotes.toscrape.com"):
        write.writerow(row)
