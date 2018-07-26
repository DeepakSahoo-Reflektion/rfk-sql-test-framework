from engine.resolver.resolver import PathResolver
from codecs import open
import os

class FileLocPathResolver(PathResolver):

    def resolve(self,file_path):

        ##TODO: use regex to identify if the file_path ends with .json then read the file or else read all .json files recursively
        ## TODO: error and exception handling , return string instead of file

        f = open(file_path, 'r', encoding='utf-8')
        file_string = f.read()
        return file_string

