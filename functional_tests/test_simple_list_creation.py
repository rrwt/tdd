from selenium import webdriver

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
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
