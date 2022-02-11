from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_input_inventory_and_retrieve_it_later(self):
        # The page for the inventory management system
        self.browser.get(self.live_server_url)

        # Page title includes Chemical Inventory
        self.assertIn('Chemical Inventory', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Current Inventory', header_text)

        # Invited to add a new chemical
        # Adds Hexanes with Barcode 1234 (CAS #110-54-3)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter Chemical')

        inputbox.send_keys('Hexanes')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Hexanes')

        inputbox = self.browser.find_element_by_id('id_new_item')

        inputbox.send_keys('Acetone')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('Acetone')
        self.wait_for_row_in_list_table('Hexanes')

        # self.fail("Finish The Test!")
        # Inputs the receipt date

        # Leaves open date blank

        # Adds Volume

        # Adds Supplier Name

        # Adds Lot Number

        # Scans Barcode

        # Marks chemical as used up

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # SEB starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Hexanes')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('Hexanes')

        # Inventory has unique URL
        chem_inv_url = self.browser.current_url
        self.assertRegex(chem_inv_url, '/inventory_management/.+')

        # new user, gen_inv, comes to site
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # gen_inv does not see chem_inv
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hexanes', page_text)
        self.assertNotIn('Acetone', page_text)
        
        # gen_inv inputs 500mL glass bottle
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('500mL Glass Bottle')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('500mL Glass Bottle')

        # gen_inv has its own URL
        gen_inv_url = self.browser.current_url
        self.assertRegex(gen_inv_url, '/inventory_management/.+')
        self.assertNotEqual( gen_inv_url, chem_inv_url)

        # gen_inv does not have content of chem_inv
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Hexanes', page_text)
        self.assertIn('500mL Glass Bottle', page_text)

        # sleep when these are satisfied.
