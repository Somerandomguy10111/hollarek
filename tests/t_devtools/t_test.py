from holytools.devtools import Unittest, patch_module
from tests.t_devtools.t_inspection import TestOptionalTyping
import os


class TestUnitTest(Unittest):
    def test_summary(self):
        results = TestOptionalTyping.execute_all()
        self.assertIn(f'tests ran successfully!',results.get_final_status())

class RealCar:
    def drive(self):
        return "Driving the Real Car"

class FakeCar:
    def drive(self):
        return "Driving the Fake Car"

class File:
    def __init__(self, fpath):
        self.fpath = fpath

    def write(self, content):
        print(f"Writing {content} to {self.fpath}")

class CustomFile:
    def write(self, content : str):
        return f'Pranked!'


class TestPatchMechanism(Unittest):
    # noinspection PyNoneFunctionAssignment
    @patch_module(File.write, CustomFile.write)
    def test_imported_cls(self):
        file_instance = File(fpath='any')
        output = file_instance.write(content='this content')
        self.assertEqual(output, "Pranked!")

    @patch_module(RealCar.drive, FakeCar().drive)
    def test_main_file_cls(self):
        car = RealCar()
        result = car.drive()
        self.assertEqual(result, "Driving the Fake Car")

    # noinspection PyNoneFunctionAssignment
    @patch_module(print, lambda *args,**kwargs : args[0])
    def test_builtin(self):
        output = print("Hello, world!")
        self.assertEqual(output, "Hello, world!")

    @patch_module(os.path.abspath, lambda *args, **kwargs : '/fake/path')
    def test_stdlib_function(self):
        result = os.path.abspath("anything")
        self.assertEqual(result, "/fake/path")

if __name__ == "__main__":
    TestPatchMechanism.execute_all()