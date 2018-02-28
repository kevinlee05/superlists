from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from unittest import skip
import os
import time
import unittest

MAX_WAIT = 10 #set the maximum amount of time we’re prepared to wait

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        #virtual display for pythonanywhere
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            print(staging_server)
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()
        #close virtual display
        self.display.stop()

    def wait_for_row_in_list_table(self, row_text):
        # add explicit waits to the test
        start_time = time.time()
        while True:
            try:
                # modified from check_for_row_in_list_table
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                """
                There are two types of exceptions we want to catch: WebDriverException for when the page hasn’t loaded and Selenium can’t find the table element on the page, and AssertionError for when the table is there, but it’s perhaps a table from before the page reloads, so it doesn’t have our row in yet.
                """
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


