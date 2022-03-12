from marshmallow import Schema, fields

class EventSchema(Schema):
    Year = fields.Int(required=True)
    ID = fields.Str(required=True)

class CacheSizeSchema(Schema):
    Items = fields.Int(required=True)
    Bytes = fields.Int(required=True)

class LopperSchema(Schema):
    Name = fields.Str(default='')
    Nation = fields.Str(default='')
    Sex = fields.Str(required=True)
    Group = fields.Str(default='')
    Bib = fields.Str(default='')

class OverallSchema(Schema):
    Time = fields.Str(required=True)
    Place = fields.Int(required=True)
    StartGroup = fields.Str(default='')

class ResultSchema(Schema):
    Year = fields.Int(required=True)
    Place = fields.Int(required=True)
    Lopper = fields.Nested(LopperSchema, required=True)
    Overall = fields.Nested(OverallSchema, required=True)