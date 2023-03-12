from enum import Enum
from datetime import datetime, timedelta
from pydantic import BaseModel


class Sex(str, Enum):
    M = 'M'
    W = 'W'

    @staticmethod
    def Parse(ageClass):
        if (ageClass is None) or not ageClass.startswith('D'):
            return Sex.M
        else:
            return Sex.W

class ResultItem(BaseModel):
    Place: int
    Sex: str
    Url: str


class RaceItem(BaseModel):
    Event: str
    Year: int
    Status: str


class LopperItem(BaseModel):
    Name: str
    Nation: str | None
    Sex: Sex | None
    Group: str | None
    Bib: str | None
    StartGroup: str | None
    PlaceOverall: int | None


class ResultDetail(BaseModel):
    Race: RaceItem
    Lopper: LopperItem
    Split: str
    Time: str
    Place: int

    @staticmethod
    def Make(kvp):
        # the race
        race = RaceItem(
            Event = kvp.get('Event'),
            Year = _try_make_int(kvp.get('Year')),
            Status = kvp.get('Race Status') or None
        )
        # the lopper
        placeTotal = _try_make_int(kvp.get('Place (Total)'))
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        ageClass = kvp.get('Group')
        lopper = LopperItem(
            Name = name,
            Nation = nation,
            Sex = Sex.Parse(ageClass),
            Group = ageClass,
            Bib = kvp.get('Number'),
            StartGroup = kvp.get('Start Group'),
            PlaceOverall = placeTotal)
        # result detail
        time = kvp.get('Time Total (Brutto)')
        return ResultDetail(
            Race = race,
            Lopper = lopper,
            Split = 'Finish',
            Time = time,
            Place = _try_make_int(kvp.get('Place'))
        )
    

def _try_make_int(value: str) -> int | None:
    if value != None and value.isdigit():
        return int(value)
    else:
        return None
