import datetime as dt
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, Any
from .utils import try_make_int, try_make_timedelta

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

    def flatten(self) -> dict[str, Any]:
        return self.model_dump(exclude={'Name'})


class LopperItem(BaseModel):
    Name: str
    Nation: str | None
    Sex: Sex | None
    Group: str | None
    Bib: str | None
    StartGroup: str | None
    PlaceOverall: int | None

    def flatten(self) -> dict[str, Any]:
        dump = self.model_dump(exclude_none=True)
        dump['Sex'] = dump['Sex'].value
        return dump


class SplitItem(BaseModel):
    Split: str
    Time: dt.timedelta | None
    Place: int

    def flatten(self) -> dict[str, Any]:
        return {f'Time_{self.Split}': self.Time, f'Place_{self.Split}': self.Place}


class ResultDetail(BaseModel):
    Race: RaceItem
    Lopper: LopperItem
    Splits: list[SplitItem]

    def flatten(self) -> dict[str, Any]:
        splits = {}
        for s in self.Splits:
            splits.update(s.flatten())
        return self.Race.flatten() | self.Lopper.flatten() | splits

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
        index = kvp['Name'].rfind('(')
        if index != -1:
            name = kvp['Name'][:index].rstrip(' ')
            nation = kvp['Name'][index+1:-1].rstrip(')')
        else:
            name = kvp['Name']
            nation = None
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
            Splits = [SplitItem(Split=s[0], Time=try_make_timedelta(s[1]), Place=try_make_int(s[2])) for s in splits]
        )