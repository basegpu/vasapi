import requests, re
from bs4 import BeautifulSoup
from .models import ResultDetail, ResultItem, Sex
from .utils import *

class VasaloppetResultsWrapper:
    BASE_URL = 'https://results.vasaloppet.se/2022/'

    def __init__(self):
        self.__eventDic = {}
        url = VasaloppetResultsWrapper.MakeUrlFromQuery('?', 'list')
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

    def FindEventIdForYear(self, year) -> str:
        return self.__eventDic[year]

    def FindResultForYearSexPlace(self, year, sex, place) -> ResultDetail:
        event = self.FindEventIdForYear(year)
        item = VasaloppetResultsWrapper.FindResultItem(event, sex, place)
        return VasaloppetResultsWrapper.GetResult(item.Url)

    def GetLopperList(self, year, size = 0) -> list:
        event = self.FindEventIdForYear(year)
        page = 0
        tableRows = []
        loppers = []
        while len(loppers) < size or size == 0:
            if len(tableRows) > 0:
                row = tableRows.pop(0)
                candidate = VasaloppetResultsWrapper.ParseResultRow(row)
                if candidate is not None:
                    loppers.append(candidate)
            else:
                page += 1
                log_to_console('loading page %i from year %i'%(page, year))
                url = VasaloppetResultsWrapper.MakeUrlFromQuery('?page=%i&event=%s&lang=EN_CAP'%(page, event), 'search')
                tableRows = VasaloppetResultsWrapper.ParseResultTable(url)
                if tableRows is None:
                    break
        return loppers

    @staticmethod
    def FindResultItem(event, sex, place) -> ResultItem:
        item = VasaloppetResultsWrapper.GetResultItem(event, sex, place)
        # hack for buggy shifting in html list
        while item.Place != place:
                placeCorr = place + (place - item.Place)
                item = VasaloppetResultsWrapper.GetResultItem(event, sex, placeCorr)
        return item

    @staticmethod
    def GetResult(url) -> ResultDetail:
        kvp = VasaloppetResultsWrapper.ParseResult(url)
        return ResultDetail.Make(kvp)

    @staticmethod
    def GetResultItem(eventID, sex, place) -> ResultItem:
        resultsPerPage = 100
        page = (place-1)/resultsPerPage + 1
        url = VasaloppetResultsWrapper.MakeUrlFromQuery('?event=%s&num_results=%i&page=%i&search[sex]=%s'%(eventID, resultsPerPage, page, sex.name), 'list')
        rows = VasaloppetResultsWrapper.ParseResultTable(url)
        iRow = (place-1)%resultsPerPage
        row = rows[iRow]
        return VasaloppetResultsWrapper.ParseResultRow(row)

    @staticmethod
    def ParseResultTable(tableUrl) -> list:
        soup = VasaloppetResultsWrapper.MakeSoupFromUrl(tableUrl)
        rows = soup.find_all('li', class_='row')[1::] # skip header row
        # make sure that first row is not an error
        if rows[0].find('div', class_='alert') is None:
            return rows
        else:
            return None

    @staticmethod
    def ParseResultRow(row) -> ResultItem:
        try:
            place = int(row.find('div', class_='numeric').get_text())
        except:
            return None
        linkCell = row.find('h4', class_='type-fullname')
        detailQuery = linkCell.find("a", href=True)["href"]
        sex = row.find('div', class_='type-age_class').get_text()
        return ResultItem(place, Sex.Parse(sex), VasaloppetResultsWrapper.MakeUrlFromQuery(detailQuery))

    @staticmethod
    def ParseResult(resultUrl) -> dict:
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
    def MakeSoupFromUrl(url) -> BeautifulSoup:
        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html,'html.parser')

    @staticmethod
    def MakeUrlFromQuery(query='', pid=None) -> str:
        url = '%s%s'%(VasaloppetResultsWrapper.BASE_URL, query)
        if pid is not None:
            url += '&pid=%s'%pid
        return url
