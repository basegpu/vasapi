import requests, re
from bs4 import BeautifulSoup, Tag
from typing import Tuple
from .models import ResultDetail, Sex
from .interfaces import IDataProvider
from .utils import try_make_int
from . import logger


class VasaloppetScraper(IDataProvider):
    BASE_URL = 'https://results.vasaloppet.se/2023/'

    def __init__(self) -> None:
        self.__eventDic = {}
        url = VasaloppetScraper.MakeUrlFromQuery('?', 'list')
        logger.info('loading event data from: ' + url)
        soup = VasaloppetScraper.MakeSoupFromUrl(url)
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

    def GetResult(self, year, sex, place) -> list[ResultDetail]:
        event = self.FindEventIdForYear(year)
        url = VasaloppetScraper.FindResult(event, sex, place)
        return VasaloppetScraper.LoadResult(url)

    def GetInitList(self, year: int, limit = 0, pages = None) -> list:
        event = self.FindEventIdForYear(year)
        page = 0
        tableRows = []
        urls = []
        while len(urls) < limit or limit == 0:
            if len(tableRows) > 0:
                row = tableRows.pop(0)
                url, _ = VasaloppetScraper.ParseResultRow(row)
                urls.append(url)
            else:
                page += 1
                logger.info('loading page %i from year %i'%(page, year))
                url = VasaloppetScraper.MakeUrlFromQuery('?page=%i&event=%s&lang=EN_CAP'%(page, event), 'search')
                tableRows = VasaloppetScraper.ParseResultTable(url)
                if tableRows is None:
                    break
        return urls

    def FindEventIdForYear(self, year: int) -> str:
        return self.__eventDic[year]

    @staticmethod
    def FindResult(event: str, sex: Sex, place: int) -> str:
        url, foundPlace = VasaloppetScraper.GetResultRow(event, sex, place)
        # hack for buggy shifting in html list
        while foundPlace != place:
                placeCorr = place + (place - item.Place)
                url, foundPlace = VasaloppetScraper.GetResultRow(event, sex, placeCorr)
        return url

    @staticmethod
    def LoadResult(url: str) -> ResultDetail:
        soup = VasaloppetScraper.MakeSoupFromUrl(url)
        details = soup.find('div', class_='detail')
        tables = details.find_all('table', class_='table')
        kvp = VasaloppetScraper.ParseOverallResult(tables)
        splits = VasaloppetScraper.ParseSplitResult(tables)
        if len(splits) == 0:
            place = try_make_int(kvp.get('Place'))
            if place is not None:
                splits.append(('Finish', kvp.get('Time Total (Brutto)'), place))
        return ResultDetail.Make(kvp, splits)

    @staticmethod
    def ParseOverallResult(tables: list[Tag]) -> dict[str, str]:
        kvp = {}
        for t in tables:
            if 'table-striped' not in t['class']:
                rows = t.tbody.find_all('tr')
                for r in rows:
                    th = r.find('th')
                    td = r.find('td')
                    if th and td:
                        kvp[th.get_text()] = td.get_text()
        return kvp
    
    @staticmethod
    def ParseSplitResult(tables: list[Tag]) -> list[Tuple[str, str, int]]:
        splits = []
        for t in tables:
            if 'table-striped' in t['class']:
                for row in t.find('tbody').findAll('tr'):
                    split = row.find('th', class_='desc')
                    time = row.find('td', class_='time')
                    place = row.find('td', class_='place right last')
                    if place is not None:
                        place = place.get_text()
                        if try_make_int(place) is not None:
                            splits.append((split.get_text(), time.get_text(), place))
        return splits

    @staticmethod
    def GetResultRow(eventID: str, sex: Sex, place: int) -> Tuple[str, int]:
        resultsPerPage = 100
        page = (place-1)/resultsPerPage + 1
        url = VasaloppetScraper.MakeUrlFromQuery('?event=%s&num_results=%i&page=%i&search[sex]=%s'%(eventID, resultsPerPage, page, sex.name), 'list')
        rows = VasaloppetScraper.ParseResultTable(url)
        iRow = (place-1)%resultsPerPage
        row = rows[iRow]
        return VasaloppetScraper.ParseResultRow(row)

    @staticmethod
    def ParseResultTable(tableUrl: str) -> list:
        soup = VasaloppetScraper.MakeSoupFromUrl(tableUrl)
        rows = soup.find_all('li', class_='row')[1::] # skip header row
        # make sure that first row is not an error
        if rows[0].find('div', class_='alert') is None:
            return rows
        else:
            return None

    @staticmethod
    def ParseResultRow(row) -> Tuple[str, int]:
        try:
            place = int(row.find('div', class_='numeric').get_text())
        except:
            place = None
        linkCell = row.find('h4', class_='type-fullname')
        detailQuery = linkCell.find("a", href=True)["href"]
        url = VasaloppetScraper.MakeUrlFromQuery(detailQuery)
        return (url, place)

    @staticmethod
    def MakeSoupFromUrl(url: str) -> BeautifulSoup:
        response = requests.get(url)
        html = response.text
        return BeautifulSoup(html,'html.parser')

    @staticmethod
    def MakeUrlFromQuery(query='', pid=None) -> str:
        url = '%s%s'%(VasaloppetScraper.BASE_URL, query)
        if pid is not None:
            url += '&pid=%s'%pid
        return url
