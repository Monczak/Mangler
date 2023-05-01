from marshmallow import Schema, fields


class TextgenSchema(Schema):
    input_id = fields.String(required=True)
    train_depths = fields.List(fields.Integer(), required=True)
    gen_depth = fields.Integer(required=True)
    seed = fields.String(required=True)
    length = fields.Integer(load_default=10000)


class TextgenCacheConfigSchema(Schema):
    cache_locked_retries = fields.Integer(required=True, data_key="CacheLockedRetries")
    retry_delay = fields.Integer(required=True, data_key="RetryDelay")

class TextgenConfigSchema(Schema):
    cache = fields.Nested(TextgenCacheConfigSchema, required=True, data_key="FreqdictCache")

