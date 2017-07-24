from selenium import webdriver
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
        self.fail('Finish the test!')

        #user is invited to enter a todo item straight away

# user types "buy peacock feathres" into a text box

# when user hits enter, page updates and page lists the item in the todo list

# there is still a textbox inviting her to add another item. user enters
# "use peacock feathers to make a fly"

# page updates and shows both items on list

# site has generated a uniqur URL for user with some explanatory text

# user visits the URL

# user quits

if __name__ == '__main__':
    unittest.main(warnings='ignore')

