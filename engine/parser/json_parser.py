from engine.parser.config_parser import ConfigParser
import json
from engine.data.sheet import TestSheet

class JsonParser(ConfigParser):

    def __init__(self):
        pass

    # def object_decoder(obj):
    #     if '__type__' in obj and obj['__type__'] == 'TestSheet':
    #         return TestSheet(obj)
    #     return obj


    def parse(self, json_file):
        print('JsonParser with file as :{}',json_file)
        ##o = json.loads(json_file)
        json_obj = json.loads(json_file,object_hook=TestSheet)
        ##print(o['name'])
        ##return o
        print(json_obj)
        print(dir(json_obj))
        print('====',json_obj.tests[0].name)
        return json_obj


