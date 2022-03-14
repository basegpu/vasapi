from enum import Enum
from dataclasses import dataclass

class Sex(Enum):
    M = 1
    W = 2

    @staticmethod
    def Parse(ageClass):
        if ageClass.startswith('D'):
            return Sex.W
        else:
            return Sex.M

@dataclass
class Event:
    Year: int
    ID: str

@dataclass
class ResultItem:
    Place: int
    Sex: str
    Url: str

@dataclass
class CacheSize:
    Items: int
    Bytes: int

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
    Bib: str

@dataclass
class ResultDetail:
    Year: int
    Place: int
    Lopper: LopperItem
    Overall: OverallItem

    @staticmethod
    def Make(kvp):
        if kvp['Race Status'] != 'Finished':
            return None
        placeTotal = kvp.get('Place (Total)')
        if placeTotal is not None:
            placeTotal = int(placeTotal)
        overall = OverallItem(kvp['Time Total (Brutto)'], placeTotal, kvp.get('Start Group'))
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        ageClass = kvp.get('Group')
        lopper = LopperItem(name, nation, Sex.Parse(ageClass), ageClass, kvp.get('Number'))
        return ResultDetail(int(kvp['Year']), int(kvp['Place']), lopper, overall)
