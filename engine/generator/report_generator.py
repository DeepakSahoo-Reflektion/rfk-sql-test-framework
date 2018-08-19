import logging
from engine.generator.generator import Generator

LOGGER = logging.getLogger(__name__)

##TODO
class ReportGenerator(Generator):
    '''
    Generator implementation for creating report.
    The data here will act as a Command object. It will contain-
        - the data to be put into the report.
        - the format in which the report to generate.
    '''

    def generate(self, data):
        pass

