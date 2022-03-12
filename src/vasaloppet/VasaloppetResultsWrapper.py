import requests, re
from bs4 import BeautifulSoup
from .models import Result
from .utils import *

class VasaloppetResultsWrapper:
    BASE_URL = 'https://results.vasaloppet.se/2022/'

    def __init__(self):
        self.__eventDic = {}
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

    def FindEventIdForYear(self, year):
        return self.__eventDic[year]

    def FindResultForYearSexPlace(self, year, sex, place):
        event = self.FindEventIdForYear(year)
        return VasaloppetResultsWrapper.LoadResult(event, sex, place)

    @staticmethod
    def LoadResult(event, sex, place):
        url, placeFound = VasaloppetResultsWrapper.GetResultUrl(event, sex, place)
        # hack for buggy shifting in html list
        while placeFound != place:
                placeCorr = place + (place - placeFound)
                url, placeFound = VasaloppetResultsWrapper.GetResultUrl(event, sex, placeCorr)
        kvp = VasaloppetResultsWrapper.ParseResult(url)
        return Result.Make(sex, kvp)

    @staticmethod
    def GetResultUrl(eventID, sex, place):
        resultsPerPage = 100
        page = (place-1)/resultsPerPage + 1
        url = VasaloppetResultsWrapper.MakeUrlFromQuery('?event=%s&num_results=%i&page=%i&search[sex]=%s'%(eventID, resultsPerPage, page, sex.name), isList=True)
        soup = VasaloppetResultsWrapper.MakeSoupFromUrl(url)
        rows = soup.find_all('li', class_='row')[1::] # skip header row
        iRow = (place-1)%resultsPerPage
        row = rows[iRow]
        place = int(row.find('div', class_='numeric').get_text())
        linkCell = row.find('h4', class_='type-fullname')
        detailQuery = linkCell.find("a", href=True)["href"]
        return (VasaloppetResultsWrapper.MakeUrlFromQuery(detailQuery), place)

    @staticmethod
    def ParseResult(resultUrl):
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
        return kvp

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
