from enum import Enum
from pydantic import BaseModel
from typing import Tuple, Any
from flatten_json import flatten
from .utils import try_make_int

class Sex(str, Enum):
    M = 'M'
    W = 'W'

    @staticmethod
    def Parse(ageClass):
        if (ageClass is None) or not ageClass.startswith('D'):
            return Sex.M
        else:
            return Sex.W


class RaceItem(BaseModel):
    Name: str
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


class SplitItem(BaseModel):
    Split: str
    Time: str
    Place: int


class ResultDetail(BaseModel):
    Race: RaceItem
    Lopper: LopperItem
    Splits: list[SplitItem]

    def flatten(self) -> dict[str, Any]:
        return flatten(self.dict())

    @staticmethod
    def Make(kvp: dict[str, str], splits: list[Tuple[str, str, int]]):
        # the race
        race = RaceItem(
            Name = kvp.get('Event'),
            Year = try_make_int(kvp.get('Year')),
            Status = kvp.get('Race Status') or None
        )
        # the lopper
        placeTotal = try_make_int(kvp.get('Place (Total)'))
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
        return ResultDetail(
            Race = race,
            Lopper = lopper,
            Splits = [SplitItem(Split=s[0], Time=s[1], Place=s[2]) for s in splits]
        )