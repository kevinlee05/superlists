from django.test import LiveServerTestCase
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest

MAX_WAIT = 10 #set the maximum amount of time we’re prepared to wait

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        #virtual display for pythonanywhere
        self.display = Display(visible=0, size=(1024, 768))
        self.display.start()
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        #close virtual display
        self.display.stop()

    def check_for_row_in_list_table(self, row_text):
        # replaced with wait_for_row_in_list_table
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

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

    def test_can_start_a_list_and_retrieve_it_later(self):
        #user has heard about new online todo app.
        #user goes to homepage
        #self.browser.get('http://klee05.pythonanywhere.com')
        self.browser.get(self.live_server_url)

        #user notices the page title and header mention todo-lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #user is invited to enter a todo item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
            )
        # user types "buy peacock feathres" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # when user hits enter, page updates and page lists the item in the todo list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #time.sleep(1)
        #self.check_for_row_in_list_table('1: Buy peacock feathers')
        #table = self.browser.find_element_by_id('id_list_table')

        # there is still a textbox inviting her to add another item. user enters
        # "use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #page updates and shows the second item on the list
        #self.check_for_row_in_list_table('1: Buy peacock feathers')
        #self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')


        self.fail('Finish the test!')

        # site has generated a unique URL for user with some explanatory text

        # user visits the URL

# user quits

if __name__ == '__main__':
    unittest.main(warnings='ignore')

