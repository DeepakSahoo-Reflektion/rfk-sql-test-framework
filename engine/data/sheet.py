
## TODO : make this as ABC
class GenericSheet:
    pass

class TestSheet:

    def __init__(self,dict):
        print('dict',dict)
        vars(self).update(dict)

    # def __init__(self,obj,**kwargs):
    #     self.name = None
    #     self.before_once = kwargs.get('before_once',None)
    #     self.before_each = kwargs.get('before_each',None)
    #     self.after_once = kwargs.get('after_once',None)
    #     self.after_each = kwargs.get('after_each',None)
    #     self.cases = kwargs.get('tests',None)
    #     self.connection = kwargs['connection']
    #
    #     self.validate()

    ## TODO: validate other test-sheet attributes for empty or 0 check , or incorrect format etc.
    def validate(self):
        ## TODO
        if not self.cases or len(self.cases) == 0:
            raise ValueError


