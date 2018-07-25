
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

    # def _set_attributes_(self,dict):
    #     pass



        ## execute the test-sheet
        ##self.execute()


    # def setup_module(self):
    #     pass
    #
    # def teardown_module(self):
    #     pass
    #
    # def before_once(self):
    #     pass
    #
    # def before_each(self):
    #     pass
    #
    # def after_once(self):
    #     pass
    #
    # def after_each(self):
    #     pass
    #
    # ## TODO: proper arguments and result from each Testcase
    # def execute(self):
    #     self.before_once()
    #
    #     for case in self.cases:
    #         self.before_each()
    #         case()
    #         self.after_each()
    #
    #     self.after_once()




