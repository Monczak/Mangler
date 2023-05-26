import yaml

from pathlib import Path

from marshmallow import ValidationError
from yaml.parser import ParserError

from schema import ExampleMetadataSchema 


METADATA_FILE_NAME = "metadata.yml"


class ExampleError(Exception):
    pass



class ExampleLoader:
    def __init__(self, path):
        self.path = Path(path)

    def parse_yaml(self, text):
        try:
            data = yaml.safe_load(text)
        except ParserError as err:
            raise ExampleError(f"Invalid YAML in file: {str(err)}")

        schema = ExampleMetadataSchema()
        try:
            parsed_data = schema.load(data)
        except ValidationError as err:
            raise ExampleError(f"Could not parse config file:\n"
                          + "\n".join([f"{field}: {msgs}" for field, msgs in err.messages_dict.items()]))
        
        return parsed_data


    def load_examples(self):
        if self.path.is_dir():
            metadata_path = self.path / METADATA_FILE_NAME
            if metadata_path.is_file():
                with open(metadata_path, "r") as file:
                    example_data = self.parse_yaml(file.read())

                    for file_name in example_data["examples"]:
                        if not Path(self.path / file_name).with_suffix(".txt").is_file():
                            raise ExampleError(f"File {file_name}.txt (defined in metadata) not found")
                    return example_data
            else:
                raise FileNotFoundError(f"{METADATA_FILE_NAME} not found")
        else:
            raise FileNotFoundError("example directory not found")
