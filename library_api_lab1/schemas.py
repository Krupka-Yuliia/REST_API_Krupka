from marshmallow import Schema, fields, validate


class BookSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    author = fields.String(required=True, validate=validate.Length(min=1, max=100))
    year = fields.Integer(required=True, validate=validate.Range(min=1500, max=2025))
    publisher = fields.String(required=True, validate=validate.Length(min=1, max=100))

