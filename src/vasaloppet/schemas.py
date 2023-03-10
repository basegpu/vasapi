from marshmallow import Schema, fields


class RaceSchema(Schema):
    Event = fields.Str(required=True)
    Year = fields.Int(required=True)
    Status = fields.Str(required=True)

class LopperSchema(Schema):
    Name = fields.Str(required=True)
    Nation = fields.Str(allow_none=True)
    Sex = fields.Str(allow_none=True)
    Group = fields.Str(allow_none=True)
    Bib = fields.Str(allow_none=True)
    StartGroup = fields.Str(allow_none=True)
    PlaceOverall = fields.Int(allow_none=True)

class ResultSchema(Schema):
    Race = fields.Nested(RaceSchema, required=True)
    Lopper = fields.Nested(LopperSchema, required=True)
    Split = fields.Str(required=True)
    Time = fields.Str(required=True)
    Place = fields.Int(required=True)
    