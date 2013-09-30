import time
sleep_time = 2
import development
import random
import datetime


## -- filler text functions --##
def rand_name(append):
    random_name = ''
    for i in range(10):
        random_name += random.choice('thequickbrownfoxjumpsoverthelazydog')
    return append + random_name


def random_text(num, **kwargs):
    letters = 'thequickbrownfoxjumpsoverthelazydog'
    if 'spaces' in kwargs:
        letters += '       '
    ret = ''
    for i in range(num):
        ret += random.choice(letters)
    return ret


## -- form entry functions -- ##
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


##-- registration test functions --##
def go_to_reg_page(self):
    reg_link = self.browser.find_element_by_link_text('Register')
    reg_link.click()
    time.sleep(sleep_time)


def admin_login(self):
    username = self.browser.find_element_by_name('username')
    username.send_keys(development.admin_user)
    password = self.browser.find_element_by_name('password')
    password.send_keys(development.admin_password)
    password.submit()
    time.sleep(sleep_time)


### -- farm test functions -- ###
def get_to_farm_index(self):
    time.sleep(sleep_time)
    farm_link = self.browser.find_element_by_link_text('Farms')
    farm_link.click()
    time.sleep(sleep_time)


def get_to_new_farm(self):
    get_to_farm_index(self)
    new_farm_link = self.browser.find_element_by_link_text('New Farm')
    new_farm_link.click()
    time.sleep(sleep_time)


def look_at_random_farm(self):
    get_to_farm_index(self)
    farm_list = self.browser.find_elements_by_partial_link_text('farm ')
    farm_link = farm_list[random.choice(range(len(farm_list)))]
    name = farm_link.text
    farm_link.click()
    time.sleep(sleep_time)
    return name


def edit_random_farm(self):
    name = look_at_random_farm(self)
    edit_link = self.browser.find_element_by_link_text('Edit this Farm')
    edit_link.click()
    time.sleep(sleep_time)
    return name


##-- glean test functions --##
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


def get_to_glean_detail(self):
    get_to_glean_index(self)
    gleans = self.browser.find_elements_by_partial_link_text('glean')
    glean_link = random.choice(gleans)
    name = glean_link.text
    glean_link.click()
    time.sleep(sleep_time)
    return name


def create_new_glean(self, **kwargs):
    get_to_new_glean(self)
    title = fill_out_identifier(self, 'glean', 'title')
    if 'timedelta' in kwargs:
        fill_out_date_element(self, kwargs['timedelta'], 'date')
    else:
        fill_out_date_element(self, 1, 'date')
    fill_out_text_elements(self,
                           10,
                           'time',
                           )
    desc = self.browser.find_element_by_id('id_description')
    desc.send_keys(random_text(250, spaces=True))
    if 'maximum' in kwargs:
        fill_out_selector_elements(self, 'time_of_day', 'farm')
    btn = self.browser.find_element_by_css_selector(
        'input[type="submit"]')
    btn.click()
    time.sleep(sleep_time)
    return title


def get_to_edit_glean_page(self, **kwargs):
    title = create_new_glean(self, **kwargs)
    edit = self.browser.find_element_by_partial_link_text('Edit Glean')
    edit.click()
    time.sleep(sleep_time)
    return title
