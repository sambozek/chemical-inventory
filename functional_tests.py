from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_input_inventory_and_retrieve_it_later(self):
        # The page for the inventory management system
        self.browser.get('http://localhost:8000')

        # Page title includes Chemical Inventory
        self.assertIn('Chemical Inventory', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Current Inventory', header_text)

        # Invited to add a new chemical
        # Adds Hexanes (CAS #110-54-3)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter Chemical')

        inputbox.send_keys('Hexanes')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('Hexanes')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Acetone')
        inputbox.send_keys
        time.sleep(1)

        self.check_for_row_in_list_table('Hexanes')
        self.check_for_row_in_list_table('Acetone')

        self.fail("Finish The Test!")
        # Inputs the receipt date

        # Leaves open date blank

        # Adds Volume

        # Adds Supplier Name

        # Adds Lot Number

        # Scans Barcode

        # Marks chemical as used up

if __name__ == '__main__':
    unittest.main()