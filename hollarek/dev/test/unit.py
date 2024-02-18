import logging
import unittest
from unittest.result import TestResult

from hollarek.dev.test.test_runners import CustomTestResult, CustomTestRunner
from hollarek.dev.log import get_logger, update_default_log_settings, LogSettings
from abc import ABC, abstractmethod
# ---------------------------------------------------------


class Unittest(unittest.TestCase, ABC):
    _logger = get_logger(settings=LogSettings(include_call_location=False))

    @abstractmethod
    def setUp(self):
        pass

    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            self.fail(f"Test failed with error: {e}")


    @classmethod
    def run_tests(cls):
        cls._print_header()
        results = cls._get_test_results()
        cls.log(cls._get_final_status_msg(result=results))


    @classmethod
    def _get_test_results(cls) -> TestResult:
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = CustomTestRunner(resultclass=CustomTestResult, verbosity=2)
        return runner.run(suite)

    @classmethod
    def _print_header(cls):
        name_info = f'  Test suite for \"{cls.__name__}\"  '
        line_len = max(CustomTestResult.test_spaces + CustomTestResult.status_spaces - len(name_info), 0)
        lines = '-' * int(line_len/2.)
        cls.log(f'{lines}{name_info}{lines}\n')


    @staticmethod
    def _get_final_status_msg(result) -> str:
        total_tests = result.testsRun
        errors = len(result.errors)
        failures = len(result.failures)
        successful_tests = total_tests - errors - failures

        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        CHECKMARK = '✓'
        CROSS = '❌'

        if errors + failures == 0:
            final_status = f"{GREEN}\n{CHECKMARK} {successful_tests}/{total_tests} tests ran successfully!{RESET}"
        else:
            final_status = f"{RED}\n{CROSS} {total_tests - successful_tests}/{total_tests} tests had errors or failures!{RESET}"

        return final_status


    @classmethod
    def log(cls,msg : str):
        cls._logger.log(msg=msg,level=logging.INFO)


if __name__ == "__main__":
    update_default_log_settings(new_settings=LogSettings(include_call_location=False))
    Unittest.run_tests()

    log_func = get_logger()