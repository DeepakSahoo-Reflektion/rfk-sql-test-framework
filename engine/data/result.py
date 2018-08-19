class SheetResult(object):
    def __init__(self, status=None, failed_cases=[]):
        self.status = status
        self.failed_cases = failed_cases

    def __repr__(self):
        return 'SheetResult(status={},failed_cases={})'.format(self.status, self.failed_cases)


class CaseResult(object):
    def __init__(self, status=None, failed_asserts=[], skipped_asserts=[]):
        self.status = status
        self.failed_asserts = failed_asserts
        self.skipped_asserts = skipped_asserts

    def get_status(self):
        return self.status

    def __repr__(self):
        return 'CaseResult(status={},failed_asserts={},skipped_asserts={})'.format(self.status, self.failed_asserts,
                                                                                   self.skipped_asserts)


class AssertResult(object):
    def __init__(self, message=None, status=None, expected=None, actual=None):
        self.message = message
        self.status = status
        self.expected = expected
        self.actual = actual

    def get_status(self):
        return self.status

    def __repr__(self):
        return 'AssertResult(message={},status={})'.format(self.message, self.status)
