import pytest
import re
from vasaloppet.VasaloppetResultsWrapper import *

def test_wrapper_init():
    wrapper = VasaloppetResultsWrapper()

def test_wrapper_get_event():
    wrapper = VasaloppetResultsWrapper()
    event = wrapper.FindEventIdForYear(2022)
    assert re.match('VL_\d+', event)

@pytest.mark.parametrize("sex,place,expected_group,expected_bib",[
    (Sex.M, 3363, 'VL6', '6222'),
    (Sex.M, 1, 'VL0', 'M15'),
    (Sex.W, 100, 'VL4', '20204'),
    (Sex.W, 101, 'VL4', '20142')
    ])
def test_wrapper_get_result_2022(sex, place, expected_group, expected_bib):
    wrapper = VasaloppetResultsWrapper()
    result = wrapper.FindResultForYearSexPlace(2022, sex, place)
    assert result.Year == 2022
    assert result.Overall.StartGroup == expected_group
    assert result.Lopper.Bib == expected_bib
