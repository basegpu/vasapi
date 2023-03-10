from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

class Sex(Enum):
    M = 1
    W = 2

    @staticmethod
    def Parse(ageClass):
        if (ageClass is None) or not ageClass.startswith('D'):
            return Sex.M
        else:
            return Sex.W

@dataclass
class ResultItem:
    Place: int
    Sex: str
    Url: str

@dataclass
class RaceItem:
    Event: str
    Year: int
    Status: str

@dataclass
class LopperItem:
    Name: str
    Nation: str
    Sex: Sex
    Group: str
    Bib: str
    StartGroup: str
    PlaceOverall: int

@dataclass
class ResultDetail:
    Race: RaceItem
    Lopper: LopperItem
    Split: str
    Time: str
    Place: int

    @staticmethod
    def Make(kvp):
        # the race
        race = RaceItem(
            kvp.get('Event'),
            _try_make_int(kvp.get('Year')),
            kvp.get('Race Status') or None)
        # the lopper
        placeTotal = _try_make_int(kvp.get('Place (Total)'))
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        ageClass = kvp.get('Group')
        lopper = LopperItem(
            name,
            nation,
            Sex.Parse(ageClass),
            ageClass,
            kvp.get('Number'),
            kvp.get('Start Group'),
            placeTotal)
        # result detail
        time = kvp.get('Time Total (Brutto)')
        return ResultDetail(
            race,
            lopper,
            'Finish',
            time,
            _try_make_int(kvp.get('Place')))
    

def _try_make_int(value: str) -> int | None:
    if value != None and value.isdigit():
        return int(value)
    else:
        return None
