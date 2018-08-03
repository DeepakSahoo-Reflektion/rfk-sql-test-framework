class SheetResult(object):
    def __init__(self, name, status=None):
        self.name = name
        self.status = status
        self.cases = {}

    def add_case_result(self, seq_no, case_result):
        self.cases[seq_no] = case_result

    def update_status(self, status):
        self.status = status

    def __repr__(self):
        return 'SheetResult(name={},status={},cases={})'.format(self.name, self.status, self.cases)


class CaseResult(object):
    def __init__(self, name=None, status=None):
        self.name = name
        self.status = status
        self.asserts = {}

    def add_assert_result(self, seq_no, assert_result):
        self.asserts[seq_no] = assert_result

    def update_status(self, status):
        self.status = status

    def __repr__(self):
        return 'CaseResult(name={},status={},asserts={})'.format(self.name, self.status, self.asserts)


class AssertResult(object):
    def __init__(self, message=None, status=None, expected=None, actual=None):
        self.message = message
        self.status = status
        self.expected = expected
        self.actual = actual

    def __repr__(self):
        return 'AssertResult(message={},status={})'.format(self.message, self.status)
