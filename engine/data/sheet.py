class TestSheet:

    def __init__(self,dict):
        print('dict',dict)
        vars(self).update(dict)

    ## TODO: validate other test-sheet attributes for empty or 0 check , or incorrect format etc.
    def validate(self):
        if not self.cases or len(self.cases) == 0:
            raise ValueError


