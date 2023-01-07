# selenium. No sessionStorage involved.
import unittest
import os
import pathlib
from time import sleep # wait for the web to run.
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

def uri(filename):        
    return pathlib.Path(os.path.abspath("templates")).as_uri() + f"/{filename}"

chrome = webdriver.Chrome()
ac = ActionChains(chrome)
# 当前网址 chrome.current_url
# 浏览器名称 chrome.name
# html = chrome.page_source
# 下一頁 chrome.forward()
# chrome.title

class NO_sessionStorage_involved(unittest.TestCase):
    
    def test_1(self): #1
        
        chrome.get(uri("1.html"))
        num = chrome.find_element(By.ID, "now_num")
        num.send_keys(1) # output would be str. Or just use "1".
        self.assertEqual(num.get_attribute("value"), "1")
        
        chrome.refresh() # Elements must be reread.
        num = chrome.find_element(By.ID, "now_num")
        self.assertEqual(num.get_attribute("value"), "")  

class Test_countdown(unittest.TestCase): # not working.
    
    def test_login_countdown_1(self): #2
        
        chrome.get(uri("layout.html")) # element only found on layout.html
        #sleep(2)
        t0 = chrome.find_element(By.CSS_SELECTOR, 'h2').text
        #sleep(3)
        t1 = chrome.find_element(By.XPATH, '//h2').text
        self.assertNotEqual(t0, t1)

class Test_text_change(unittest.TestCase):
    
    def test_label_1(self): #3
        
        chrome.get(uri("1.html"))
        sleep(2)
        erase = chrome.find_element(By.CLASS_NAME, "erase")
        labeltext = chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]').get_attribute("innerHTML") # or .text
        ac.move_to_element(erase).perform() # erase.onmouseover
        self.assertNotEqual(labeltext, chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]').get_attribute("innerHTML"))

if __name__ == "__main__":
    
    unittest.main()    
        
class Test_button_click(unittest.TestCase): # click() doesn't work at all.  

    def test_back_button_11(self): #3
        
        chrome.get(uri("11.html"))
        origin = chrome.current_url
        back = chrome.find_element(By.ID, "back")
        self.assertTrue(EC.element_to_be_clickable(back)) # found.
        back.click() # no work.
        self.assertNotEqual(origin, chrome.current_url)
        chrome.back() # works.
        self.assertEqual(origin, chrome.current_url)

    def test_erase_button_1(self): #1
        
        chrome.get(uri("1.html"))
        date = chrome.find_element(By.ID, "pickup_date")
        num = chrome.find_element(By.ID, "now_num")
        Select(date).select_by_index("1") # 0: explanation.
        # = Select(date).select_by_value("today {{today}}")?
        # = Select(date).select_by_visible_text("")
        #num.submit()
        #num.clear()
        num.send_keys("1") # > 0, <= product inventory.
        self.assertIn("today", date.get_attribute("value"))
        self.assertEqual(num.get_attribute("value"), "1") # value != .text
        
        erase = chrome.find_element(By.CLASS_NAME, "erase") # or By.NAME
        self.assertTrue(EC.element_to_be_clickable(erase))
        # ac.click(erase).perform(), erase.click(), execute_script and erase.send_keys(Keys.ENTER) all failed.
        erase.click()
        self.assertEqual(date.get_attribute("value"), "")
        self.assertEqual(num.get_attribute("value"), "")
        # NO chrome.close() or chrome.quit() yet.
    
    def test_erase_button_11(self): #2
        
        chrome.get(uri("11.html"))
        pickup_time = chrome.find_element(By.ID, "pickup_time")
        contact = chrome.find_element(By.ID, "contact")
        phone = chrome.find_element(By.ID, "phone")
        title = chrome.find_element(By.ID, "title")
        
        Select(pickup_time).select_by_index("1") # 0: explanation.
        contact.send_keys("contact")
        phone.send_keys("phone numbers")
        title.send_keys("title surname")
        
        RM = chrome.find_element(By.ID, "RememberMe")
        self.assertTrue(EC.element_to_be_clickable(RM)) # found.
        self.assertTrue(RM.is_selected())
        self.assertFalse(RM.is_enabled())
        
        erase = chrome.find_element(By.CLASS_NAME, "erase") # or By.NAME
        self.assertTrue(EC.element_to_be_clickable(erase)) # found.
        erase.click()
        
        self.assertEqual(pickup_time.get_attribute("value"), "")
        self.assertEqual(contact.get_attribute("value"), "")    
        self.assertEqual(phone.get_attribute("value"), "")
        self.assertEqual(title.get_attribute("value"), "")
        self.assertEqual(contact.get_attribute("value"), "")
        self.assertTrue(RM.is_enabled())
        self.assertFalse(RM.is_selected()) 