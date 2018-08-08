import logging

from common.const.vars import CASE, SHEET, SUITE, ASSERT

logger = logging.getLogger(__name__)


class ContextManager(object):
    """
    This class is responsible to manage and create different kinds of contexts.
    """

    @staticmethod
    def initialize_default(type=None):
        if not type:
            return

        if type == CASE:
            return CaseContext().with_default()
        elif type == SHEET:
            return SheetContext().with_default()
        elif type == SUITE:
            return SuiteContext().with_default()
        elif type == ASSERT:
            return AssertContext().with_default()
        else:
            logger.error('ContextManager:failed to create context,Invalid type..')
            raise Exception('Invalid context type')


class SuiteContext(object):
    def with_default(self):
        self.data = None
        self.params = {}
        self.contexts = {}
        self.instances = {}
        self.result = None
        return self

    def update_params(self, params):
        self.params.update(params)
        return self

    def get_param(self, param_name):
        return self.params.get(param_name, None)

    def get_params(self, param_names):
        return {p: self.params.get(p, None) for p in param_names}

    def update_contexts(self, params):
        self.contexts.update(params)
        return self

    def update_instances(self, params):
        self.instances.update(params)
        return self

    def get_instance(self, param):
        return self.instances.get(param, None)

    def update_data(self, param):
        self.data = param
        return self

    def get_data(self):
        return self.data

    def update_result(self, param):
        self.result = param
        return self


## TODO:visit here again
class SheetContext(object):
    def with_default(self):
        self.data = None
        self.params = {}
        self.contexts = {}
        self.instances = {}
        self.result = None
        return self

    def update_params(self, params):
        self.params.update(params)
        return self

    def get_param(self, param_name):
        return self.params.get(param_name, None)

    def get_params(self, param_names):
        return {p: self.params.get(p, None) for p in param_names}

    def update_contexts(self, params):
        self.contexts.update(params)
        return self

    def update_instances(self, params):
        self.instances.update(params)
        return self

    def get_instance(self, param):
        return self.instances.get(param, None)

    def update_data(self, param):
        self.data = param
        return self

    def get_data(self):
        return self.data

    def update_result(self, param):
        self.result = param
        return self


class CaseContext(object):
    def with_default(self):
        self.data = None
        self.params = {}
        self.instances = {}
        self.contexts = {}
        self.result = None
        return self

    def update_data(self, param):
        self.data = param
        return self

    def get_data(self):
        return self.data

    def update_params(self, params):
        self.params.update(params)
        return self

    def get_param(self, param_name):
        return self.params.get(param_name, None)

    def get_params(self, param_names):
        return {p: self.params.get(p, None) for p in param_names}

    def update_instances(self, params):
        self.instances.update(params)
        return self

    def get_instance(self, param):
        return self.instances.get(param, None)

    def update_contexts(self, params):
        self.contexts.update(params)
        return self

    def update_result(self, param):
        self.result = param
        return self


class AssertContext(object):
    def with_default(self):
        self.data = None
        self.params = {}
        self.instances = {}
        self.result = None
        return self

    def update_data(self, param):
        self.data = param
        return self

    def get_data(self):
        return self.data

    def update_params(self, params):
        self.params.update(params)
        return self

    def get_param(self, param_name):
        return self.params.get(param_name, None)

    def get_params(self, param_names):
        return {p: self.params.get(p, None) for p in param_names}

    def update_instances(self, params):
        self.instances.update(params)
        return self

    def get_instance(self, param):
        return self.instances.get(param, None)

    def update_result(self, param):
        self.result = param
        return self
