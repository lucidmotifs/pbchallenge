import os, time, sys, unittest
from django.test import TestCase
from testrunner.forms import TestRunInstanceForm, TestRunForm

import logging
logname = "testrunner.tests.ui.{}".format(os.path.basename(__file__).replace(".py", ".log"))
logging.basicConfig(
    filename=logname,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG)

class StaticTestCase(TestCase):
    def setUp(self):
        logging.info("Setting up")

    def tearDown(self):
        logging.info("Tearing down")

    def test_testrun_instance_fields(self):
        logging.info("Sleeping 2")
        time.sleep(2)
        self.assertTrue(True)

    def test_dummy_pass(self):
        logging.info("Passing")
        self.assertTrue(1 == 1)

    def test_dummy_delayed(self):
        logging.info("Passing and sleeping 12")
        time.sleep(12)

        self.assertTrue(True)
