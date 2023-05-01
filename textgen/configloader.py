from tomllib import loads, TOMLDecodeError

from marshmallow import ValidationError


class ConfigError(Exception):
    def __init__(self, message=None):
        self.message = message
    
    def __str__(self):
        return self.message


def load_toml(path, schema):
    with open(path, "r") as file:
        data = loads(file.read())
        config = schema.load(data)
        return config


def parse_toml(path, schema):
    try:
        config = load_toml(path, schema)
        return config
    except FileNotFoundError:
        raise ConfigError(f"Could not find config file at {path}")
    except TOMLDecodeError as err:
        raise ConfigError(f"Invalid TOML in config file: {str(err)}")
    except ValidationError as err:
        raise ConfigError(f"Could not parse config file:\n"
                          + "\n".join([f"{field}: {msgs}" for field, msgs in err.messages_dict.items()]))
    