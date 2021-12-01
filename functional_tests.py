from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_input_inventory_and_retrieve_it_later(self):
        # The page for the inventory management system
        self.browser.get('http://localhost:8000')

        # Page title includes Chemical Inventory
        self.assertIn('Chemical Inventory', self.browser.title)
        self.fail('Complete the test!')

        # Invited to add a new chemical
        # Adds Hexanes (CAS #110-54-3)

        # Inputs the receipt date

        # Leaves open date blank

        # Adds Volume

        # Adds Supplier Name

        # Adds Lot Number

        # Scans Barcode

if __name__ == '__main__':
    unittest.main()