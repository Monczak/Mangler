from marshmallow import Schema, fields


class TextgenSchema(Schema):
    input_id = fields.String(required=True)
    train_depths = fields.List(fields.Integer(), required=True)
    gen_depth = fields.Integer(required=True)
    seed = fields.String(required=True)
    length = fields.Integer(load_default=10000)
