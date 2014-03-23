import unittest
import time
from selenium import webdriver

from selenium_test_functions import (admin_login,
                                     go_to_reg_page,
                                     sleep_time,
                                     )


class EntryAndFrontPage(unittest.TestCase):

    def tearDown(self):
        self.browser.quit()
        time.sleep(sleep_time)

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:8000')
        time.sleep(sleep_time)

    def test_front_page_renders(self):
        self.assertNotEqual(self.browser.title,
                            'Problem loading page',
                            'Browser Title Indicates 404 on Home')

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
        self.browser = webdriver.Chrome()
        self.browser.get('http://localhost:8000')
        time.sleep(sleep_time)

    def tearDown(self):
        self.browser.quit()
        time.sleep(sleep_time)

    def test_registration_page_renders(self):
        go_to_reg_page(self)
        self.assertIn('Sign Up', self.browser.title)

    def test_registration_page_renders(self):
        go_to_reg_page(self)
