import logging
##TODO: parse the query result in Assert_handler
##TODO: create the sql and expected using the script_path in Assert_handler
##TODO: if needed create separate Result class to return the results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class SheetHandler(object):
    '''
    This is a COR pattern implementation of our execution sequence. one execution delegates the process to another
    one instead of doing it all alone.
    '''

    def __init__(self,service):
        logger.info('SheetHandler:init')
        self._service = service
        self._handler = CaseHandler(service)
        self._results = {}
        self._meta_args = {}

    def _create_meta_args(self,test_sheet):
        logger.info('SheetHandler:_create_meta_args ENTRY with %s', test_sheet)
        ##print(getattr(test_sheet,'name'))
        ##logger.info('dir(sheet)',dir(test_sheet))
        ##logger.info('dict sheet',test_sheet.__dict__)
        ##sheet_name = test_sheet.__getattribute__('name')
        # sheet_name = getattr(test_sheet,'name')
        # sql_path = test_sheet.__getattribute__('sql_path')
        # script_path = test_sheet.__getattribute__('script_path')
        # self._meta_args['sheet_name'] = sheet_name
        # self._meta_args['sql_path'] = sql_path
        # self._meta_args['script_path'] = script_path

        self._meta_args['sheet_name'] =  test_sheet.get('name',None)
        self._meta_args['sql_path'] = test_sheet.get('sql_path',None)
        self._meta_args['script_path'] = test_sheet.get('script_path',None)
        logger.info('SheetHandler:_create_meta_args EXIT with %s', test_sheet)

    def handle_request(self,test_sheet):
        logger.info('SheetHandler:handle_request ENTRY with %s',test_sheet)
        self._create_meta_args(test_sheet)
        #self._service.serve(test_sheet.__getattribute__('before_once'))
        self._service.serve(test_sheet.get('before_once',None))

        #for case in test_sheet.__getattribute__('tests'):
        for case in test_sheet.get('tests',None):
            self._service.serve(test_sheet.get('before_each', None))
            #self._service.serve(test_sheet.__getattribute__('before_each'))

            #case_name = case.__getattribute__('name')
            case_name = case.get('name',None)
            case_result = self._handler.handle_request(case,self._meta_args)
            self._results[case_name] = case_result

            #self._service.serve(test_sheet.__getattribute__('after_each'))
            self._service.serve(test_sheet.get('after_each', None))

        #self._service.serve(test_sheet.__getattribute__('after_once'))
        self._service.serve(test_sheet.get('after_once', None))

        return self._results

class CaseHandler(object):

    def __init__(self,service):
        logger.info('CaseHandler:init')
        self._service = service
        self._handler = AssertHandler(service)
        self._result = {}

    def handle_request(self,test_case,meta_args):
        logger.info('CaseHandler:handle_request ENTRY with %s', test_case)
        #self._service.serve(test_case.__getattribute__('before_test'))
        self._service.serve(test_case.get('before_test', None))

        self._service.serve(meta_args['script_path'])
        count = 0
        #for each_assert in test_case.__getattribute__('asserts'):
        for each_assert in test_case.get('asserts', None):

            assert_result = self._handler.handle_request(each_assert,meta_args)
            self._result['assert-{}'.format(count)]=assert_result
            count += 1

        ##self._service.serve(test_case.__getattribute__('after_test'))
        self._service.serve(test_case.get('after_test', None))
        return self._result


## TODO: to change the sql query replace enricher with a decorator
class AssertHandler(object):

    def __init__(self,service):
        logger.info('AssertHandler:init')
        self._service = service
        self._result = None

    def content_enrich(self,args):
        pass


    def handle_request(self,each_assert,meta_args):
        #self._service.serve(each_assert.__getattribute__('expected'))
        self._service.serve(each_assert.get('expected', None))

        ##encriched_sql_query = self.content_enrich(each_assert.__getattribute__('sql'))
        sql_query = each_assert.get('sql', None)
        query_result = self._service.serve(sql_query)


        self._result = query_result
        return self._result

