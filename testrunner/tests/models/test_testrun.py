import time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

class TestRunTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_testrun_instance_fields(self):
        self.assertTrue(True)

    def test_dummy_fail(self):
        self.assertTrue(False)

    def test_dummy_exception(self):
        raise TypeError

    def test_dummy_delayed(self):
        time.sleep(20)

        self.assertTrue(True)
