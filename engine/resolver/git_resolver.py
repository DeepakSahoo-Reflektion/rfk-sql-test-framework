from engine.resolver.resolver import PathResolver

##TODO: establish the connection and access check etc for git inisde init block
class GitPathResolver(PathResolver):

    def __init__(self):
        pass

    def resolve(self,file_path):
        f = open(file_path, 'r', encoding='utf-8')
        file_string = f.read()
        f.close()
        return file_string