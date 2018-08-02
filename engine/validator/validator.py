from common.const.vars import XUNIT,BEFORE_ONCE,BEFORE_EACH,AFTER_ONCE,AFTER_EACH


class ValidatorFactory:
    _instances = {}

    @staticmethod
    def get_validator(type=None):
        if not type:
            return

        if type == XUNIT:
            validator = ValidatorFactory._instances.get(type, None)
            if not validator:
                validator = XUnitValidator()
                ValidatorFactory._instances[type] = validator
            return validator

        else:
            return None


class XUnitValidator:
    optional_attrs = [BEFORE_ONCE, BEFORE_EACH,AFTER_EACH,AFTER_ONCE]
    mandatory_attrs = ["name", "script_path", "tests"]

    def validate(self, arg):
        for attr in XUnitValidator.mandatory_attrs:
            if attr not in arg.keys():
                raise Exception('Validation Error:Missing attribute')
