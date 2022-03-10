from enum import Enum

class Sex(Enum):
    M = 1
    W = 2

class Event:
    def __init__(self, year, eventID):
        self.Year = year
        self.ID = eventID

class Overall:
    def __init__(self, time, startGroup, place):
        self.Time = time
        self.Place = place
        self.StartGroup = startGroup

class Lopper:
    def __init__(self, name, nation, sex, group, bib):
        self.Name = name
        self.Nation = nation
        self.Sex = sex
        self.Group = group
        self.Bib = bib

class Result:
    def __init__(self, year, place, lopper, overall):
        self.Year = year
        self.Place = place
        self.Lopper = lopper
        self.Overall = overall

    @staticmethod
    def Make(sex, kvp):
        if kvp['Race Status'] != 'Finished':
            return None
        placeTotal = kvp.get('Place (Total)')
        if placeTotal is not None:
            placeTotal = int(placeTotal)
        overall = Overall(kvp['Time Total (Brutto)'], kvp.get('Start Group'), placeTotal)
        nameAndNation = kvp['Name'].rstrip(')').split('(')
        name = nameAndNation[0].rstrip(' ')
        nation = nameAndNation[1]
        lopper = Lopper(name, nation, sex.name, kvp.get('Group'), kvp.get('Number'))
        return Result(int(kvp['Year']), int(kvp['Place']), lopper, overall)
