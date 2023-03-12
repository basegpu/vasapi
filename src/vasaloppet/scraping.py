import requests, re
from bs4 import BeautifulSoup
from .models import ResultDetail, ResultItem, Sex
from .interfaces import IDataProvider
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

    def GetResult(self, year, sex, place) -> ResultDetail:
        event = self.FindEventIdForYear(year)
        item = VasaloppetScraper.FindResultItem(event, sex, place)
        return VasaloppetScraper.LoadResult(item.Url)

    def GetInitList(self, year: int, limit = 0, pages = None) -> list:
        event = self.FindEventIdForYear(year)
        page = 0
        tableRows = []
        urls = []
        while len(urls) < limit or limit == 0:
            if len(tableRows) > 0:
                row = tableRows.pop(0)
                candidate = VasaloppetScraper.ParseResultRow(row)
                if candidate is not None:
                    urls.append(candidate.Url)
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
    def FindResultItem(event: str, sex: Sex, place: int) -> ResultItem:
        item = VasaloppetScraper.GetResultItem(event, sex, place)
        # hack for buggy shifting in html list
        while item.Place != place:
                placeCorr = place + (place - item.Place)
                item = VasaloppetScraper.GetResultItem(event, sex, placeCorr)
        return item

    @staticmethod
    def LoadRow(url: str) -> dict[str, str]:
        return VasaloppetScraper.ParseResult(url)

    @staticmethod
    def LoadResult(url: str) -> ResultDetail:
        kvp = VasaloppetScraper.LoadRow(url)
        return ResultDetail.Make(kvp)

    @staticmethod
    def GetResultItem(eventID: str, sex: Sex, place: int) -> ResultItem:
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
    def ParseResultRow(row) -> ResultItem:
        try:
            place = int(row.find('div', class_='numeric').get_text())
        except:
            return None
        linkCell = row.find('h4', class_='type-fullname')
        detailQuery = linkCell.find("a", href=True)["href"]
        sex = row.find('div', class_='type-age_class').get_text()
        return ResultItem(
            Place = place,
            Sex = sex,
            Url = VasaloppetScraper.MakeUrlFromQuery(detailQuery)
        )

    @staticmethod
    def ParseResult(resultUrl: str) -> dict:
        soup = VasaloppetScraper.MakeSoupFromUrl(resultUrl)
        details = soup.find('div', class_='detail')
        tables = details.find_all('table', class_='table')
        kvp = {}
        for t in tables:
            if 'table-striped' in t['class']:
                pass
                #print('parsing the split table ...')
            else:
                rows = t.tbody.find_all('tr')
                for r in rows:
                    th = r.find('th')
                    td = r.find('td')
                    if th and td:
                        kvp[th.get_text()] = td.get_text()
        return kvp

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
