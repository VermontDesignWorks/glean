import unittest
import random
import datetime
#from django.utils import timezone


from selenium import webdriver

import time

from selenium_test_functions import (admin_login,
                                     get_to_farm_index,
                                     get_to_new_farm,
                                     look_at_random_farm,
                                     edit_random_farm,
                                     rand_name,
                                     go_to_reg_page,
                                     get_to_glean_index,
                                     get_to_new_glean,
                                     get_to_glean_detail,
                                     create_new_glean,
                                     get_to_edit_glean_page,
                                     random_text,
                                     fill_out_identifier,
                                     fill_out_text_elements,
                                     fill_out_num_elements,
                                     fill_out_selector_elements,
                                     fill_out_date_element,
                                     sleep_time)


class GleanEventPageCrud(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000')
        time.sleep(sleep_time)

    def tearDown(self):
        self.browser.quit()
        time.sleep(sleep_time)

    def test_glean_index_request_resolves(self):
        #admin_login(self)
        get_to_glean_index(self)
        self.assertIn('Index', self.browser.title)

    def test_minimum_glean_can_be_created(self):
        title = create_new_glean(self, )
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, h2.text)

    def test_maximum_glean_can_be_created(self):
        title = create_new_glean(self, maximum=True)
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, h2.text)

    def test_glean_detail_page_renders(self):
        title = get_to_glean_detail(self)
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, h2.text)

    def test_future_glean_has_edit_glean_button(self):
        title = create_new_glean(self, timedelta=5)
        try:
            edit = self.browser.find_element_by_partial_link_text('Edit Glean')
        except:
            edit = None
        self.assertIsNotNone(edit)

    def test_future_glean_can_be_edited(self):
        title = get_to_edit_glean_page(self, timedelta=5)
        title2 = fill_out_identifier(self, 'glean', 'title')
        btn = self.browser.find_element_by_css_selector(
            'input[type="submit"]')
        btn.click()
        time.sleep(sleep_time)
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertNotEqual(title, h2.text)

    def test_past_glean_has_no_edit_glean_button(self):
        title = create_new_glean(self, timedelta=-5)
        try:
            edit = self.browser.find_element_by_partial_link_text('Edit Glean')
        except:
            edit = None
        self.assertIsNone(edit)
