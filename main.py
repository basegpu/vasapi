import random
import requests
from bs4 import BeautifulSoup
import re


def main():
    print(FindEventIdForYear(2020))
    

def MakeSoupForUrl(url):
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html,'html.parser')

def FindEventIdForYear(year):
    url = 'https://results.vasaloppet.se/2022/?pid=list'
    soup = MakeSoupForUrl(url)
    eventPattern = re.compile("Vasaloppet (Winter )?\d{4}$")
    racePattern = re.compile("Vasaloppet$")
    eventDic = {}
    for g in soup.find_all('optgroup'):
        label = g['label']
        if eventPattern.match(label):
            y = int(label[-4::])
            for o in g.find_all('option'):
                if racePattern.match(o.get_text()):
                    eventDic[y] = o['value']
    return eventDic[year]

if __name__ == '__main__':
    main()