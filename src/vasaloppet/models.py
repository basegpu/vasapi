from enum import Enum
from dataclasses import dataclass

class Sex(Enum):
    M = 1
    W = 2

@dataclass
class Event:
    Year: int
    ID: str

@dataclass
class OverallItem:
    Time: str
    Place: int
    StartGroup: str

@dataclass
class LopperItem:
    Name: str
    Nation: str
    Sex: str
    Group: str
    Bib: int

@dataclass
class Result:
    Year: int
    Place: int
    Lopper: LopperItem
    Overall: OverallItem

    @staticmethod
    def Make(sex, kvp):
        if kvp['Race Status'] != 'Finished':
            return None
        placeTotal = kvp.get('Place (Total)')
        if placeTotal is not None:
            placeTotal = int(placeTotal)
        overall = OverallItem(kvp['Time Total (Brutto)'], placeTotal, kvp.get('Start Group'))
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        lopper = LopperItem(name, nation, sex.name, kvp.get('Group'), kvp.get('Number'))
        return Result(int(kvp['Year']), int(kvp['Place']), lopper, overall)
