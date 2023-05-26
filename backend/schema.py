from marshmallow import Schema, fields


class BackendRateLimitConfigSchema(Schema):
    upload = fields.String(required=True, data_key="Upload")


class BackendFileLimitConfigSchema(Schema):
    upload_file_count = fields.Integer(required=True, data_key="UploadFileCount")
    max_file_size = fields.Integer(required=True, data_key="MaxFileSize")


class BackendCleanupConfigSchema(Schema):
    uploads_cleanup_interval = fields.Integer(required=True, data_key="UploadsCleanupInterval")
    uploads_min_lifetime = fields.Integer(required=True, data_key="UploadsMinLifetime")
    generated_cleanup_interval = fields.Integer(required=False, data_key="GeneratedCleanupInterval")
    generated_min_lifetime = fields.Integer(required=False, data_key="GeneratedMinLifetime")


class BackendConfigSchema(Schema):
    rate_limits = fields.Nested(BackendRateLimitConfigSchema, required=True, data_key="RateLimits")
    file_limits = fields.Nested(BackendFileLimitConfigSchema, required=True, data_key="FileLimits")
    cleanup = fields.Nested(BackendCleanupConfigSchema, required=True, data_key="Cleanup")


class ExampleTextSchema(Schema):
    title = fields.String(required=True)
    author = fields.String(required=False)
    lang = fields.String(required=True)
    tags = fields.List(fields.String(), required=True)


class ExampleMetadataSchema(Schema):
    examples = fields.Dict(keys=fields.String(), values=fields.Nested(ExampleTextSchema))
