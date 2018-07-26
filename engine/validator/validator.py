class JsonValidator:

    def validate(self,test_sheet):
        try:

            test_sheet.__getattribute__('before_once')
        except AttributeError:
            print('Missing Value')
