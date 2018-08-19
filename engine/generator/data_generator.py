import logging
from engine.generator.generator import Generator
from common.const.error_codes import error_data_conversion

LOGGER = logging.getLogger(__name__)


class DataGenerator(Generator):
    '''
    Child implementation class of the Generator.
    Main purpose of this class is to provide implementation for data generation from the expected output.
    '''
    def str2tupleList(self, s):
        return eval("[%s]" % s)

    def convert_to_tuple_if_already_not(self, data):
        result = self.str2tupleList(data)
        return [tuple([result[i]]) for i in range(0, len(result)) if not isinstance(result[i], tuple)]

    def generate(self, data):
        try:
            enriched_input = self.convert_to_tuple_if_already_not(data)

            if len(enriched_input) == 0:
                enriched_input = data
        except Exception as e:
            LOGGER.error('Error while converting the expected data.')
            raise Exception("{}-{}".format(error_data_conversion[0], error_data_conversion[1]))
        return enriched_input
