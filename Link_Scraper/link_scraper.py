import csv
from bs4 import BeautifulSoup
import requests
from time import sleep


def scraper(base):
    links = [base]
    # stop = False
    # while base:
    request = requests.get(f"{base}")
    soup = BeautifulSoup(request.text, "html.parser")
    all_links = soup.find_all('a')
    # get the quotes
    for link in all_links:
        link_text = f"{base}{link['href']}"
        # print(link_text)
        if link_text not in links and link['href'] != '/':
            links.append(link_text)
            # sleep(1)
            links.extend(scraper(link_text))

    return links


if __name__ == "__main__":
    with open("quotes.txt", "w") as file:
        website = input('What website would you like to scrape?: ')
        links_list = scraper(website)
        print(links_list)
        for one_link in links_list:
            file.write(f'{one_link}\n')
        file.close()


