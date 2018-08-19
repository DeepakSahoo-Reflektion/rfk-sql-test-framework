import logging
from common.const.error_codes import missing_mandatory_params, invalid_predicate

LOGGER = logging.getLogger(__name__)


class ResultComparator():
    comparison_types = {'value': ['greater_than', 'less_than', 'equal_to', 'not_equal_to'],
                        'list': ['equal_to', 'not_equal_to', 'is_empty', 'is_not_empty']}

    def greater_than(self, a, b):
        return True if a > b else False

    def less_than(self, a, b):
        return True if a < b else False

    def greater_than_equal(self, a, b):
        return True if a >= b else False

    def less_than_equal(self, a, b):
        return True if a <= b else False

    def equal_to(self, a, b):
        if type(a) != type(b):
            LOGGER.info('Invalid comparison types')
            return False

        if isinstance(a, tuple):
            k1 = frozenset(a)
            k2 = frozenset(b)
            return k1 == k2 and len(a) == len(b)
        return a == b

    def not_equal_to(self, a, b):
        if type(a) != type(b):
            LOGGER.info('Invalid comparison types')
            return False

        return True if a != b else False

    def is_empty(self, a):
        return True if len(a) == 0 else False

    def is_not_empty(self, a):
        return True if len(a) != 0 else False

    def compare(self, a, b, ext_comparator, type):
        if not ext_comparator or not type or not b:
            LOGGER.error('Missing mandatory parameters')
            raise Exception("{}-{}".format(missing_mandatory_params[0], missing_mandatory_params[1]))

        if ext_comparator not in ResultComparator.comparison_types[type]:
            LOGGER.error('Invalid Condition for the predicate, check the supported types')
            raise Exception("{}-{}".format(invalid_predicate[0], invalid_predicate[1]))

        func = self.__getattribute__(ext_comparator)
        LOGGER.info('inside result_compare.. with a %s b %s and ext_comparator %s and type %s', a, b, ext_comparator,
                    type)
        return func(a, b)
