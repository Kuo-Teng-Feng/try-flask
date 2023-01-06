# selenium
import unittest
import os
import pathlib
from time import sleep #time.sleep(n) # to delay the auto close for n sec.
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def uri(filename):        
    return pathlib.Path(os.path.abspath("templates")).as_uri() + f"/{filename}"

chrome = webdriver.Chrome()
    
class Test_browser(unittest.TestCase):

    def test_erase_button_1(self): #1
        
        chrome.get(uri("1.html"))
        erase = chrome.find_element(By.CLASS_NAME, "erase")
        date = chrome.find_element(By.ID, "pickup_date")
        num = chrome.find_element(By.ID, "now_num")
        
        erase.click()
        self.assertIn("?", date.text) # "Preferred...?"
        self.assertEqual(num.text, "")
    
    def test_erase_button_11(self): #2
        
        chrome.get(uri("11.html"))
        erase = chrome.find_element(By.CLASS_NAME, "erase")
        pickup_time = chrome.find_element(By.ID, "pickup_time")
        contact = chrome.find_element(By.ID, "contact")
        phone = chrome.find_element(By.ID, "phone")
        title = chrome.find_element(By.ID, "title")
        RM = chrome.find_element(By.ID, "RememberMe")
        
        erase.click()
        self.assertIn("?", pickup_time.text) # "Preferred...?"
        self.assertEqual(contact.text, "")    
        self.assertEqual(phone.text, "")
        self.assertEqual(title.text, "")
        self.assertEqual(contact.text, "")
        self.assertTrue(RM.is_enabled())
        self.assertFalse(RM.is_selected())

    def test_countdown_2(self): #3
        
        chrome.get(uri("2.html"))
        cd = chrome.find_element(By.CLASS_NAME, "countdown")
        #chrome.execute_script()
        t0 = cd.text
        sleep(5)
        self.assertNotEqual(t0, cd.text)
    
    def test_labeltext_change_1(self): #4
        
        chrome.get(uri("1.html"))
        erase = chrome.find_element(By.CLASS_NAME, "erase")
        labeltext = chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]').text              
        ac = ActionChains(chrome)
        
        ac.move_to_element(erase).perform() # erase.onmouseover
        nlabel = chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]')
        #time.sleep(2)
        self.assertNotEqual(labeltext, nlabel.get_attribute("innerHTML"))
        

if __name__ == "__main__": # must be the last.
    
    unittest.main()