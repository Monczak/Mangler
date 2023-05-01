import tomllib

def load_toml(path, schema):
    with open(path, "r") as file:
        data = tomllib.loads(file.read())
        config = schema.load(data)
        return config

    