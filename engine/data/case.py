

class TestCase:

    def __init__(self,*args,**kwargs):
        self._name = None
        self._before_test = None
        self._after_test = None
        self._asserts = None

    def __str__(self):
        pass

    ## TODO : make the TestCase class as callable
    def __call__(self, *args, **kwargs):
        self.before_test()

        self.after_test()
        pass

    def before_test(self,args):
        pass

    def after_test(self,args):
        pass

    def _asserts(self):
        pass



