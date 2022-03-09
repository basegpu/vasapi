import requests, re
from bs4 import BeautifulSoup
from enum import Enum
from .utils import *

class Sex(Enum):
    M = 1
    W = 2

class Overall:
    def __init__(self, time, startGroup, place):
        self.Time = time
        self.Place = place
        self.StartGroup = startGroup

class Lopper:
    def __init__(self, name, nation, group, bib):
        self.Name = name
        self.Nation = nation
        self.Group = group
        self.Bib = bib

class Result:
    def __init__(self, year, lopper, overall):
        self.Year = year
        self.Lopper = lopper
        self.Overall = overall

    @staticmethod
    def Make(kvp):
        if kvp['Race Status'] != 'Finished':
            return None
        overall = Overall(kvp['Time Total (Brutto)'], kvp.get('Start Group'), kvp.get('Place (Total)'))
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        lopper = Lopper(name, nation, kvp.get('Group'), kvp.get('Number'))
        return Result(int(kvp['Year']), lopper, overall)

class VasaloppetResultsWrapper:
    BASE_URL = 'https://results.vasaloppet.se/2022/'

    def __init__(self):
        url = VasaloppetResultsWrapper.MakeUrlFromQuery('?', isList=True)
        log_to_console('loading event data from: ' + url)
        soup = VasaloppetResultsWrapper.MakeSoupFromUrl(url)
        eventPattern = re.compile("Vasaloppet (Winter )?\d{4}$")
        racePattern = re.compile("Vasaloppet$")
        self.__eventDic = {}
        for g in soup.find_all('optgroup'):
            label = g['label']
            if eventPattern.match(label):
                y = int(label[-4::])
                for o in g.find_all('option'):
                    if racePattern.match(o.get_text()):
                        self.__eventDic[y] = o['value']
        log_to_console('successfully initialized vasaloppet wrapper')

    def FindEventIdForYear(self, year):
        return self.__eventDic[year]

    def GetResultUrl(self, eventID, sex, place):
        resultsPerPage = 100
        page = (place-1)/resultsPerPage + 1
        url = VasaloppetResultsWrapper.MakeUrlFromQuery('?event=%s&num_results=%i&page=%i&search[sex]=%s'%(eventID, resultsPerPage, page, sex.name), isList=True)
        soup = VasaloppetResultsWrapper.MakeSoupFromUrl(url)
        rows = soup.find_all('li', class_='row')[1::] # skip header row
        iRow = (place-1)%resultsPerPage
        linkRow = rows[iRow].find('h4', class_='type-fullname')
        detailQuery = linkRow.find("a", href=True)["href"]
        return VasaloppetResultsWrapper.MakeUrlFromQuery(detailQuery)

    def ParseResult(self, resultUrl):
        soup = VasaloppetResultsWrapper.MakeSoupFromUrl(resultUrl)
        details = soup.find('div', class_='detail')
        tables = details.find_all('table', class_='table')
        kvp = {}
        for t in tables:
            if 'table-striped' in t['class']:
                print('parsing the split table ...')
            else:
                rows = t.tbody.find_all('tr')
                for r in rows:
                    th = r.find('th')
                    td = r.find('td')
                    if th and td:
                        kvp[th.get_text()] = td.get_text()
        return Result.Make(kvp)

    @staticmethod
    def MakeSoupFromUrl(url):
        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html,'html.parser')

    @staticmethod
    def MakeUrlFromQuery(query='', isList=False):
        url = '%s%s'%(VasaloppetResultsWrapper.BASE_URL, query)
        if isList:
            url += '&pid=list'
        return url
