import pytest
import re
from vasaloppet.scraping import *
from vasaloppet.models import Sex


class TestWrapper:

    def test_init(self):
        wrapper = VasaloppetScraper()

    def test_get_event(self):
        wrapper = VasaloppetScraper()
        event = wrapper.FindEventIdForYear(2022)
        assert re.match('VL_\d+', event)
    
    @pytest.mark.parametrize("year,expected_pages",[
        (2021, 13),
        (1922, 5),
        (2024, 670)
        ])
    def test_get_number_of_result_pages(self, year, expected_pages):
        wrapper = VasaloppetScraper()
        pages = wrapper.GetNumberOfResultPages(year)
        assert pages == expected_pages
    
    @pytest.mark.parametrize("year,expected_urls",[
        (2021, 13),
        (1922, 5),
        (2024, 670)
        ])
    def test_get_result_page_urls(self, year, expected_urls):
        wrapper = VasaloppetScraper()
        urls = wrapper.GetPageUrls(year)
        assert len(urls) == expected_urls
    
    def test_get_results_from_table_url(self):
        wrapper = VasaloppetScraper()
        urls = wrapper.GetPageUrls(1922)
        results = []
        for url in urls:
            results.extend(wrapper.GetResultsFromTableUrl(url))
        assert len(results) == 117

    @pytest.mark.parametrize("sex,place,expected_group,expected_bib",[
        (Sex.M, 3364, '6', '6222'),
        (Sex.M, 1, 'Elit', 'M15'),
        (Sex.W, 100, '4', '20204'),
        (Sex.W, 101, '4', '20142')
        ])
    def test_get_result_2022(self, sex, place, expected_group, expected_bib):
        wrapper = VasaloppetScraper()
        result = wrapper.GetResult(2022, sex, place)
        assert result.Race.Year == 2022
        assert result.Lopper.StartGroup == expected_group
        assert result.Lopper.Bib == expected_bib