import pytest
import re, time
from vasaloppet.VasaloppetResultsWrapper import *
from vasaloppet.models import Sex

class TestWrapper:

    def test_init(self):
        wrapper = VasaloppetResultsWrapper()

    def test_get_event(self):
        wrapper = VasaloppetResultsWrapper()
        event = wrapper.FindEventIdForYear(2022)
        assert re.match('VL_\d+', event)

    @pytest.mark.parametrize("sex,place,expected_group,expected_bib",[
        (Sex.M, 3364, 'VL6', '6222'),
        (Sex.M, 1, 'VL0', 'M15'),
        (Sex.W, 100, 'VL4', '20204'),
        (Sex.W, 101, 'VL4', '20142')
        ])
    def test_get_result_2022(self, sex, place, expected_group, expected_bib):
        wrapper = VasaloppetResultsWrapper()
        result = wrapper.GetResult(2022, sex, place)
        assert result.Year == 2022
        assert result.Overall.StartGroup == expected_group
        assert result.Lopper.Bib == expected_bib

    @pytest.mark.parametrize("year,size,expected_size",[
        (2022, 1, 1),
        (2020, 37, 37),
        (1922, 0, 117)
        ])
    def test_get_lopper_list(self, year, size, expected_size):
        wrapper = VasaloppetResultsWrapper()
        loppers = wrapper.GetInitList(year, size)
        assert len(loppers) == expected_size