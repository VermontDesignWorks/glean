import unittest
import random
import datetime
#from django.utils import timezone


from selenium import webdriver

import time

sleep_time = 1

from selenium_test_functions import (admin_login,
                                     get_to_farm_index,
                                     get_to_new_farm,
                                     look_at_random_farm,
                                     edit_random_farm,
                                     rand_name,
                                     go_to_reg_page)


def get_to_glean_index(self):
    admin_login(self)
    index_link = self.browser.find_element_by_link_text('Gleans')
    index_link.click()
    time.sleep(sleep_time)


def get_to_new_glean(self):
    get_to_glean_index(self)
    new = self.browser.find_element_by_link_text('New Glean')
    new.click()
    time.sleep(sleep_time)


def random_text(num, **kwargs):
    letters = 'thequickbrownfoxjumpsoverthelazydog'
    if 'spaces' in kwargs:
        letters += '       '
    ret = ''
    for i in range(num):
        ret += random.choice(letters)
    return ret


def fill_out_identifier(self, kind, descriptor):
    ret = "{0} {1}".format(kind, random_text(10))
    field = self.browser.find_element_by_name(descriptor)
    field.send_keys(ret)
    return ret


def fill_out_text_elements(self, num, *args, **kwargs):
    for arg in args:
        linku = self.browser.find_element_by_name(arg)
        if 'spaces' in kwargs:
            fake_words = random_text(num, spaces=True)
            linku.send_keys(fake_words)
        else:
            fake_words = random_text(num)
            linku.send_keys(random_text(num))


def fill_out_num_elements(self, *args):
    for arg in args:
        link = self.browser.find_element_by_name(arg)
        link.send_keys(random.choice('132456789'))


def fill_out_selector_elements(self, *args):
    for arg in args:
        link = self.browser.find_element_by_name(arg)
        options = link.find_elements_by_tag_name('option')
        options[1].click()


def fill_out_date_element(self, timedelta=0, *args):
    for arg in args:
        date = self.browser.find_element_by_name(arg)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=timedelta)
        date.send_keys(tomorrow.strftime('%m/%d/%Y'))


class GleanEventPageCrud(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get('http://localhost:8000')

    def tearDown(self):
        self.browser.quit()
        time.sleep(sleep_time)

    # def test_glean_index_request_resolves(self):
    #     #admin_login(self)
    #     get_to_glean_index(self)
    #     self.assertIn('Index', self.browser.title)

    def test_minimum_glean_can_be_created(self):
        get_to_new_glean(self)
        title = fill_out_identifier(self, 'glean', 'title')
        fill_out_date_element(self, 1, 'date')
        fill_out_text_elements(self, 10, 'time', )
        desc = self.browser.find_element_by_id('id_description')
        desc.send_keys(random_text(50, spaces=True))
        btn = self.browser.find_element_by_css_selector(
            'input[type="submit"]')
        btn.click()
        time.sleep(sleep_time)
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, h2.text)

    def test_maximum_glean_can_be_created(self):
        get_to_new_glean(self)
        title = fill_out_identifier(self, 'glean', 'title')
        fill_out_date_element(self, 1, 'date')
        fill_out_text_elements(self,
                               10,
                               'time',
                               'duration',
                               'address_one',
                               'address_two',
                               'city',
                               'zipcode')
        desc = self.browser.find_element_by_id('id_description')
        desc.send_keys(random_text(50, spaces=True))
        fill_out_selector_elements(self, 'time_of_day', 'farm')
        btn = self.browser.find_element_by_css_selector(
            'input[type="submit"]')
        btn.click()
        time.sleep(sleep_time)
        h2 = self.browser.find_element_by_tag_name('h2')
        self.assertIn(title, h2.text)
