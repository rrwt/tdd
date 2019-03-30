from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
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
        self.wait_for_row_in_list_table('1: testing')

        inputbox = self.get_inputbox()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )