import yaml
import os
from engine.parser.parser import ConfigParser

## TODO: exception handling and logging
## TODO: this type is here to parse to a specific class type , not using as of now
class YamlParser(ConfigParser):

    def parse(self, file,type = None):
        return yaml.safe_load(file)