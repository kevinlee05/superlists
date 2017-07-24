from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #user has heard about new online todo app.
        #user goes to homepage
        self.browser.get('http://klee05.pythonanywhere.com')

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
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Buy peacock feathers' for row in rows),
                "New to-do item did not appear in table"
            )

        # there is still a textbox inviting her to add another item. user enters
        # "use peacock feathers to make a fly"
        self.fail('Finish the test!')

# page updates and shows both items on list

# site has generated a uniqur URL for user with some explanatory text

# user visits the URL

# user quits

if __name__ == '__main__':
    unittest.main(warnings='ignore')

