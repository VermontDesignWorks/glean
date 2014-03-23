import unittest
import time
from selenium import webdriver

from selenium_test_functions import (admin_login,
                                     get_to_farm_index,
                                     get_to_new_farm,
                                     look_at_random_farm,
                                     edit_random_farm,
                                     rand_name,
                                     sleep_time,
                                     )


class FarmCRUD(unittest.TestCase):

    def tearDown(self):
        self.browser.quit()
        time.sleep(sleep_time)

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:8000')
        time.sleep(sleep_time)
        admin_login(self)

    def test_farm_index_renders(self):
        get_to_farm_index(self)
        self.assertIn('Farm Index', self.browser.title)

    def test_create_farm_page_renders(self):
        get_to_new_farm(self)
        self.assertIn('New Farm', self.browser.title)

    def test_new_minimum_farm(self):
        get_to_new_farm(self)
        name = self.browser.find_element_by_name('name')
        self.farm_name = rand_name('farm ')
        name.send_keys(self.farm_name)

        directions = self.browser.find_element_by_name('directions')
        directions.send_keys('These are bogus directions'
                             ' run by the Selenium to do headful testing')

        instructions = self.browser.find_element_by_name('instructions')
        instructions.send_keys('Another long typed out thingie')

        counties = self.browser.find_element_by_name('counties')
        options = counties.find_element_by_tag_name('option')
        options.click()

        address_one = self.browser.find_element_by_name('address_one')
        address_one.send_keys('100 Main Street')

        city = self.browser.find_element_by_name('city')
        city.send_keys('Springfield')

        state = self.browser.find_element_by_name('state')
        options = state.find_elements_by_tag_name('option')
        options[1].click()

        save_button = self.browser.find_element_by_id('save-button')
        save_button.click()

        self.assertIn(self.farm_name, self.browser.title)

    def test_new_full_farm(self):
        get_to_new_farm(self)
        name = self.browser.find_element_by_name('name')
        self.farm_name2 = rand_name('farm ')
        name.send_keys(self.farm_name2)

        directions = self.browser.find_element_by_name('directions')
        directions.send_keys('These are bogus directions'
                             ' run by the Selenium to do headful testing')

        instructions = self.browser.find_element_by_name('instructions')
        instructions.send_keys('Another long typed out thingie')

        counties = self.browser.find_element_by_name('counties')
        options = counties.find_element_by_tag_name('option')
        options.click()

        address_one = self.browser.find_element_by_name('address_one')
        address_one.send_keys('100 Main Street')

        address_two = self.browser.find_element_by_name('address_two')
        address_two.send_keys('Apt 3')

        city = self.browser.find_element_by_name('city')
        city.send_keys('Springfield')

        state = self.browser.find_element_by_name('state')
        options = state.find_elements_by_tag_name('option')
        options[1].click()

        zipcode = self.browser.find_element_by_name('zipcode')
        zipcode.send_keys('05674')

        p_i_m = self.browser.find_element_by_name('physical_is_mailing')
        p_i_m.click()

        description = self.browser.find_element_by_id('id_description')
        description.send_keys('Some Text for the description'
                              ' of this particular farm')

        mailing_add = self.browser.find_element_by_name('mailing_address_one')
        mailing_add.send_keys('PO Box 12123')

        mailing_ad2 = self.browser.find_element_by_name('mailing_address_two')
        mailing_ad2.send_keys('ATTN: Farmer Joe')

        mailing_city = self.browser.find_element_by_name('mailing_city')
        mailing_city.send_keys('Another long typed out thingie')

        mailing_state = self.browser.find_element_by_name('mailing_state')
        options = mailing_state.find_elements_by_tag_name('option')
        options[1].click()

        mailing_zip = self.browser.find_element_by_name('mailing_zip')
        mailing_zip.send_keys('05674')

        phone_1 = self.browser.find_element_by_name('phone_1')
        phone_1.send_keys('8885551212')

        phone_1_type = self.browser.find_element_by_name('phone_1_type')
        options = phone_1_type.find_elements_by_tag_name('option')
        options[1].click()

        phone_2 = self.browser.find_element_by_name('phone_2')
        phone_2.send_keys('8885551212')

        phone_2_type = self.browser.find_element_by_name('phone_2_type')
        options = phone_2_type.find_elements_by_tag_name('option')
        options[1].click()

        email = self.browser.find_element_by_name('email')
        email.send_keys('test@example.com')

        save_button = self.browser.find_element_by_id('save-button')
        save_button.click()
        time.sleep(3)

        self.assertIn(self.farm_name2, self.browser.title)

    def test_read_view_for_random_farm_that_already_exists(self):
        look_at_random_farm(self)
        time.sleep(sleep_time)
        self.assertIn('Details', self.browser.title)

    def test_update_view_for_random_farm_that_already_exists(self):
        edit_random_farm(self)
        self.assertIn('Edit', self.browser.title)

    def test_updating_a_random_farm_that_already_exists(self):
        edit_random_farm(self)
        name = self.browser.find_element_by_name('name')
        self.farm_name = rand_name('edited_farm ')
        name.send_keys(self.farm_name)
        save_button = self.browser.find_element_by_id('save-button')
        save_button.click()
        time.sleep(sleep_time)
        self.assertIn(self.farm_name, self.browser.title)

    def test_deleting_a_random_farm_that_already_exists(self):
        farm_name = look_at_random_farm(self)
        delete_page_link = self.browser.find_element_by_partial_link_text(
            'Delete')
        delete_page_link.click()
        time.sleep(sleep_time)
        confirm_delete = self.browser.find_element_by_css_selector(
            'input[class]')
        confirm_delete.click()
        farm_list = self.browser.find_elements_by_partial_link_text('farm ')
        farm_list = [farm.text for farm in farm_list]
        self.assertNotIn(farm_name, farm_list)
