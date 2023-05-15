from marshmallow import Schema, fields


class CheckStatusSchema(Schema):
    task_id = fields.String(required=True)


class TextgenRequestSchema(Schema):
    input_id = fields.String(required=True)
    train_depths = fields.List(fields.Integer(), required=True)
    gen_depth = fields.Integer(required=True)
    seed = fields.String(required=True)
    length = fields.Integer(load_default=10000)
    temperature = fields.Float(load_default=1)


class TextgenCacheConfigSchema(Schema):
    cache_locked_retries = fields.Integer(required=True, data_key="CacheLockedRetries")
    retry_delay = fields.Integer(required=True, data_key="RetryDelay")


class TextgenTasksConfigSchema(Schema):
    soft_time_limit = fields.Integer(required=True, data_key="TimeLimit")
    time_limit = fields.Integer(required=True, data_key="HardTimeLimit")


class TextgenTextAnalysisConfigSchema(Schema):
    progress_step = fields.Integer(required=True, data_key="ProgressStep")


class TextgenTextGenerationConfigSchema(Schema):
    buffer_size = fields.Integer(required=True, data_key="BufferSize")
    max_gen_retries = fields.Integer(required=True, data_key="MaxGenRetries")
    max_length = fields.Integer(required=True, data_key="MaxLength")
    max_depth = fields.Integer(required=True, data_key="MaxDepth")
    temp_range = fields.List(fields.Float(), required=True, data_key="TemperatureRange", validate=lambda l: len(l) == 2 and l[0] <= l[1])


class TextgenCleanupConfigSchema(Schema):
    cache_cleanup_interval = fields.Integer(required=True, data_key="CacheCleanupInterval")
    cache_min_lifetime = fields.Integer(required=True, data_key="CacheMinLifetime")
    generated_cleanup_interval = fields.Integer(required=False, data_key="GeneratedCleanupInterval")
    generated_min_lifetime = fields.Integer(required=False, data_key="GeneratedMinLifetime")


class TextgenConfigSchema(Schema):
    cache = fields.Nested(TextgenCacheConfigSchema, required=True, data_key="FreqdictCache")
    analysis = fields.Nested(TextgenTextAnalysisConfigSchema, required=True, data_key="TextAnalysis")
    textgen = fields.Nested(TextgenTextGenerationConfigSchema, required=True, data_key="TextGeneration")
    tasks = fields.Nested(TextgenTasksConfigSchema, required=True, data_key="Tasks")
    cleanup = fields.Nested(TextgenCleanupConfigSchema, required=True, data_key = "Cleanup")
