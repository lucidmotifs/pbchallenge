import os, time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

import logging
logname = "testrunner.tests.models.{}".format(os.path.basename(__file__).replace(".py", ".log"))
logging.basicConfig(
    filename=logname,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG)

class TestRunTestCase(TestCase):
    def setUp(self):
        logging.info("Setting up")

    def tearDown(self):
        logging.info("Tearing down")

    def test_testrun_instance_fields(self):
        self.assertTrue(True)

    def test_dummy_fail(self):
        logging.info("Failing")
        self.assertTrue(False)

    def test_dummy_delayed(self):
        time.sleep(20)

        self.assertTrue(True)
