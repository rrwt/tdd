import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows], f'{row_text} not found in: {rows}')
    
    def enter_text_inputbox(self, text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        self.enter_text_inputbox('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        self.enter_text_inputbox('Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        self.fail('Finish the test!')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
