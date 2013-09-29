import unittest
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import development
import time

sleep_time = 1

from selenium_test_functions import admin_login,get_to_farm_index,get_to_new_farm,look_at_random_farm,edit_random_farm,rand_name,go_to_reg_page


class EntryAndFrontPage(unittest.TestCase):

	def tearDown(self):
		self.browser.quit()
		time.sleep(sleep_time)
		
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('http://localhost:8000')

	def test_front_page_renders(self):
		self.assertNotEqual(self.browser.title, 'Problem loading page', 'Browser Title Indicates 404 on Home')

	def test_registration(self):
		register_link = self.browser.find_element_by_link_text('Register')
		register_link.click()

	def test_failed_login_works(self):
		
		username = self.browser.find_element_by_name('username')
		username.send_keys('testuser')
		password = self.browser.find_element_by_name('password')
		password.send_keys('testpassword')
		password.submit()
		self.shouldStop = True
		self.assertIn("Log", self.browser.title)

	def test_login_actually_works(self):
		admin_login(self)
		self.assertIn('Welcome', self.browser.title)



class RegisterAndConfirm(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('http://localhost:8000')

	def tearDown(self):
		self.browser.quit()
		time.sleep(sleep_time)

	def test_registration_page_renders(self):
		go_to_reg_page(self)
		self.assertIn('Sign Up', self.browser.title)

	def test_registration_page_renders(self):
		go_to_reg_page(self)


class FarmCRUD(unittest.TestCase):

	def tearDown(self):
		self.browser.quit()
		time.sleep(sleep_time)
		
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('http://localhost:8000')
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
		directions.send_keys('These are bogus directions run by the Selenium to do headful testing')

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
		directions.send_keys('These are bogus directions run by the Selenium to do headful testing')

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

		physical_is_mailing = self.browser.find_element_by_name('physical_is_mailing')
		physical_is_mailing.click()

		description = self.browser.find_element_by_id('id_description')
		description.send_keys('Some Text for the description of this particular farm')

		mailing_address_one = self.browser.find_element_by_name('mailing_address_one')
		mailing_address_one.send_keys('PO Box 12123')

		mailing_address_two = self.browser.find_element_by_name('mailing_address_two')
		mailing_address_two.send_keys('ATTN: Farmer Joe')

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

	def test_updaing_a_random_farm_that_already_exists(self):
		edit_random_farm(self)
		name = self.browser.find_element_by_name('name')
		self.farm_name = rand_name('edited_farm ')
		name.send_keys(self.farm_name)
		save_button = self.browser.find_element_by_id('save-button')
		save_button.click()
		time.sleep(sleep_time)		
		self.assertIn(self.farm_name, self.browser.title)

if __name__ == '__main__':
	unittest.main()