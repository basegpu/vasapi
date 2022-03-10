from marshmallow import Schema, fields

class EventSchema(Schema):
    Year = fields.Int(default=None)
    ID = fields.Str(default='')