import random
import requests
from bs4 import BeautifulSoup
import re



def main():
    FindEventIdForYear(2020)
    

def MakeSoupForUrl(url):
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html,'html.parser')

def FindEventIdForYear(year):
    url = 'https://results.vasaloppet.se/2022/?pid=list'
    soup = MakeSoupForUrl(url)
    pattern = re.compile("Vasaloppet (Winter )?\d{4}")
    eventDic = {}
    for g in soup.find_all('optgroup'):
        label = g['label']
        if pattern.match(label):
            eventDic[int(label[-4::])] = "vasa"
            print(g)
    print(eventDic)

if __name__ == '__main__':
    main()