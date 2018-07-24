
## TODO : make this as ABC
class GenericSheet:
    pass

class TestSheet:

    def _set_attributes_(self,dict):
        pass

    def __init__(self,**kwargs):
        self._before_once_ = kwargs.get('before_once',None)
        self._before_each = kwargs.get('before_each',None)
        self._after_once = kwargs.get('after_once',None)
        self._after_each = kwargs.get('after_each',None)
        self.cases = kwargs.get('tests',None)

        ## TODO
        if not self.cases or len(self.cases) == 0:
            raise ValueError

        ## execute the test-sheet
        self.execute()


    def setup_module(self):
        pass

    def teardown_module(self):
        pass

    def before_once(self):
        pass

    def before_each(self):
        pass

    def after_once(self):
        pass

    def after_each(self):
        pass

    ## TODO: proper arguments and result from each Testcase
    def execute(self):
        self.before_once()

        for case in self.cases:
            self.before_each()
            case()
            self.after_each()

        self.after_once()




