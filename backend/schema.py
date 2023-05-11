from marshmallow import Schema, fields


class BackendRateLimitConfigSchema(Schema):
    upload = fields.String(required=True, data_key="Upload")


class BackendFileLimitConfigSchema(Schema):
    upload_file_count = fields.Integer(required=True, data_key="UploadFileCount")
    max_file_size = fields.Integer(required=True, data_key="MaxFileSize")


class BackendConfigSchema(Schema):
    rate_limits = fields.Nested(BackendRateLimitConfigSchema, required=True, data_key="RateLimits")
    file_limits = fields.Nested(BackendFileLimitConfigSchema, required=True, data_key="FileLimits")