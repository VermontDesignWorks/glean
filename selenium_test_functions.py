import time
sleep_time = 1
import development
import random

### -- selenium test functions -- ###
def admin_login(self):
	username = self.browser.find_element_by_name('username')
	username.send_keys(development.admin_user)
	password = self.browser.find_element_by_name('password')
	password.send_keys(development.admin_password)
	password.submit()

def get_to_farm_index(self):
	time.sleep(sleep_time)
	farm_link = self.browser.find_element_by_link_text('Farms')
	farm_link.click()

def get_to_new_farm(self):
	get_to_farm_index(self)
	time.sleep(sleep_time)
	new_farm_link = self.browser.find_element_by_link_text('New Farm')
	new_farm_link.click()

def look_at_random_farm(self):
	get_to_farm_index(self)
	time.sleep(sleep_time)
	farm_list = self.browser.find_elements_by_partial_link_text('farm ')
	farm_link = farm_list[random.choice(range(len(farm_list)))]
	farm_link.click()

def edit_random_farm(self):
	look_at_random_farm(self)
	time.sleep(sleep_time)
	edit_link = self.browser.find_element_by_link_text('Edit this Farm')
	edit_link.click()

def rand_name(append):
	random_name = ''
	for i in range(10):
		random_name += random.choice('thequickbrownfoxjumpsoverthelazydog')
	return append + random_name

def go_to_reg_page(self):
	reg_link = self.browser.find_element_by_link_text('Register')
	reg_link.click()
	time.sleep(sleep_time)