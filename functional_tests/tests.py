import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


MAX_WAIT = 4


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
    
    def tearDown(self):
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        start_time = time.time()

        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows], f'{row_text} not found in: {rows}')
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    print(self.browser)
                    raise e
                
                time.sleep(0.2)
    
    def enter_text_inputbox(self, text):
        inputbox = self.get_inputbox()

        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)
    
    def get_inputbox(self):
        return self.browser.find_element_by_id('id_new_item')

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        self.enter_text_inputbox('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        self.enter_text_inputbox('Use peacock feathers to make a fly')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        
        self.enter_text_inputbox('Buy peacock feathers')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        self.assertRegex(self.browser.current_url, '/lists/.+')
        self.browser.quit()

        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        self.enter_text_inputbox('Buy Milk')
        self.check_for_row_in_list_table('1: Buy Milk')

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy Milk', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_inputbox()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10,
            msg=f'{inputbox.location["x"]}, {inputbox.size["width"]/2}'
        )

        self.enter_text_inputbox('testing')
        self.check_for_row_in_list_table('1: testing')

        inputbox = self.get_inputbox()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
