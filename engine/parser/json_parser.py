import json
from engine.parser.parser import ConfigParser

## TODO: exception handling and logging
class JsonParser(ConfigParser):

    def parse(self, file,type = None):
        if not type:
            return json.loads(file)

        json_obj = json.loads(file, object_hook=type)
        return json_obj