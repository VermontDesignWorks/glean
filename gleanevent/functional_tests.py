import unittest
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import time

sleep_time = 1

from selenium_test_functions import admin_login,get_to_farm_index,get_to_new_farm,look_at_random_farm,edit_random_farm,rand_name,go_to_reg_page

def get_to_glean_index(self):
	self.browser.find_element_by_link_text('Gleans')
	time.sleep(sleep_time)

class GleanEventPageCrud(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.FireFox()
		self.browser.get('http://localhost:8000')

	def tearDown(self):
		self.browser.quit()
		time.sleep(sleep_time)

	def test_glean_index_request_resolves(self):
		admin_login(self)
		get_to_glean_index(self)
		self.assertIn('Index', self.browser.title)