from codecs import open
import os

from engine.resolver.resolver import PathResolver

##TODO: use regex to identify if the file_path ends with .json then read the file or else read all .json files recursively
##TODO: error and exception handling , return string instead of file
##TODO: exception handling and logging
##TODO: take extra argument, so that you can read a single file or which pattern_file to search or all files etc.
class FSPathResolver(PathResolver):

    def resolve(self,file_path):
        f = open(file_path, 'r', encoding='utf-8')
        file_string = f.read()
        f.close()
        return file_string

