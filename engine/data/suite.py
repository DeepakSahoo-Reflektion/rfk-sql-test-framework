

class TestSuite:

    ## TODO : set the time to now
    def __init__(self,args):
        self._no_of_sheets = None
        self.start_time = None
        self.test_sheets = []


    def add_test_sheets(self,*sheets):
        self.test_sheets.append(sheets)

    def remove_test_sheets(self):
        pass

    def count_sheets(self):
        self._no_of_sheets += 1
        return self._no_of_sheets





