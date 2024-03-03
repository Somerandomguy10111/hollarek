import logging
from typing import Optional
import unittest
from unittest.result import TestResult

from hollarek.logging import get_logger, LogSettings, Logger
from abc import abstractmethod

from .test_runners import CustomTestResult, CustomTestRunner
# ---------------------------------------------------------

class Unittest(unittest.TestCase):
    _logger : Optional[Logger] = None


    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass


    def run(self, result=None):
        super().run(result)

    @classmethod
    def execute_all(cls, show_run_times: bool = False, show_details : bool = True):
        cls._print_header()

        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = CustomTestRunner(logger=cls.get_logger(), show_run_times=show_run_times, show_details=show_details)
        results =  runner.run(suite)
        summary = cls._get_final_status_msg(result=results)

        cls.log(summary)


    @classmethod
    def _print_header(cls):
        name_info = f'  Test suite for \"{cls.__name__}\"  '
        line_len = max(CustomTestResult.test_spaces + CustomTestResult.status_spaces - len(name_info), 0)
        lines = '=' * int(line_len/2.)
        cls.log(f'{lines}{name_info}{lines}')


    @staticmethod
    def _get_final_status_msg(result  : TestResult) -> str:
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
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = get_logger(settings=LogSettings(include_call_location=False, use_timestamp=False), name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls,msg : str):
        logger = cls.get_logger()
        logger.log(msg=msg,level=logging.INFO)


    def assertEqual(self, first, second, *args, **kwargs):
        if not first == second:
            first_str = str(first).__repr__()
            second_str =str(second).__repr__()
            raise AssertionError(f'{first_str} != {second_str}')

    def assertIn(self, member, container, msg = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            raise AssertionError(f'{member_str} not in {container_str}')