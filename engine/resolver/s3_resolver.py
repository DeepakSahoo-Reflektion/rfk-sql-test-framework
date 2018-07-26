from engine.resolver.resolver import PathResolver

##TODO: establish the connection inside __init__ to s3
class S3PathResolver(PathResolver):

    def __init__(self):
        super().__init__()


    def resolve(self,file_path):
        f = open(file_path, 'r', encoding='utf-8')
        file_string = f.read()
        f.close()
        return file_string