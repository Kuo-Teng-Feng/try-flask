# selenium. No sessionStorage involved. Nor db.
import unittest
import os
import pathlib 
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait # Important to wait for the web to run. Or: 
from time import sleep # only if there's no applicable EC for WebDriverWait.
from data import listcancelpaths
import datetime

def uri(filename):        
    return pathlib.Path(os.path.abspath("templates")).as_uri() + f"/{filename}"

chrome = webdriver.Chrome()
ac = ActionChains(chrome)

# browser name = chrome.name
# html = chrome.page_source
# next page = chrome.forward()
# page title = chrome.title

# Use "inspect" to locate elements. "view source" returns only static source code without js execution.

def fulfill_1(): # fulfill all inputs in 1.html without Key.Enter

    chrome.get(uri("1.html"))
    
    # pickup_date
    WebDriverWait(chrome, 10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_date"), is_selected=False)) # found untouched.
    Select(chrome.find_element(By.ID, "pickup_date")).select_by_index(1) # or str "1". 0: explanation. Or: Select(date).select_by_value(). Select(date).select_by_visible_text("")
    WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_selected(chrome.find_elements(By.TAG_NAME, "option")[1]))
    # Unnecessary: self.assertIn("today", date.get_attribute("value")) # value != .text(html code)
    
    # now_num
    num = chrome.find_element(By.ID, "now_num")
    WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of(num)) # found and seen.
    num.send_keys("1") # > 0, <= product inventory. Others: num.submit(). num.clear()
    WebDriverWait(chrome, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "now_num"), "1"))    
    
    # wish_num
    WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "wish_num")))
    chrome.find_element(By.ID, "wish_num").send_keys(2)
    WebDriverWait(chrome, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "wish_num"), "2"))

def fulfill_11(): # fulfill all inputs in 11.html without Key.Enter

    chrome.get(uri("11.html"))
        
    WebDriverWait(chrome, 10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_time"), is_selected=False)) # found untouched.
    Select(chrome.find_element(By.ID, "pickup_time")).select_by_index(1) # 0: explanation.
    WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_selected(chrome.find_elements(By.TAG_NAME, "option")[1]))
        
    contact = chrome.find_element(By.ID, "contact")
    WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of(contact))
    contact.send_keys("contact")
    WebDriverWait(chrome, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "contact"), "contact"))
        
    phone = chrome.find_element(By.ID, "phone")
    WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of(phone))
    phone.send_keys("phone numbers")
    WebDriverWait(chrome, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "phone"), "phone numbers"))
        
    title = chrome.find_element(By.ID, "title")
    WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of(title))
    title.send_keys("title surname")
    WebDriverWait(chrome, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "title"), "title surname"))
    
class NO_sessionStorage_involved(unittest.TestCase):
    
    def test_1(self): #1 and also 1.html
        
        fulfill_1()       
        chrome.refresh() # Elements must be reread.
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertIn("?", chrome.find_element(By.ID, "pickup_date").get_attribute("value")) # Default: "Preferred...?"
        self.assertEqual(chrome.find_element(By.ID, "now_num").get_attribute("value"), "") 
        #Or: self.assertTrue(EC.text_to_be_present_in_element_attribute((By.ID, "now_num"), "value", ""))
        #Or: self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "now_num"), ""))
  
class Test_button_click(unittest.TestCase):

    def test_back_button_11(self): #2
        
        chrome.get(uri("11.html"))
        
        origin = chrome.current_url
        back = chrome.find_element(By.ID, "back")
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(back)) # found working. Otherwise click() can fail.
        back.click()
        self.assertTrue(EC.url_changes(origin)) # Or: self.assertNotEqual(origin, chrome.current_url)
        chrome.back()
        self.assertTrue(EC.url_to_be(origin)) # Or: self.assertEqual(origin, chrome.current_url)

    def test_erase_button_1(self): #3
        
        fulfill_1()
        
        erase = chrome.find_element(By.CLASS_NAME, "erase") # or By.NAME
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(erase)) # found working.
        erase.click() # Or: ac.click(erase).perform(), execute_script, erase.send_keys(Keys.ENTER)
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "now_num"), "")) # self.assertEqual(date.get_attribute("value"), "")
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "pickup_date"), "")) # self.assertEqual(num.get_attribute("value"), "")
        
    def test_erase_button_11(self): #4
        
        fulfill_11()
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "RememberMe")))
        RM = chrome.find_element(By.ID, "RememberMe")
        # during key in title etc.: self.assertTrue(EC.element_to_be_clickable(RM)).
        # Otherwise:
        #self.assertTrue(RM.is_selected()) 
        #self.assertFalse(RM.is_enabled())
        
        erase = chrome.find_element(By.CLASS_NAME, "erase") # or By.NAME
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(erase))
        
        erase.click()
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "pickup_time"), ""))
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "contact"), ""))    
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "phone"), ""))
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "title"), ""))
        self.assertTrue(RM.is_enabled())
        self.assertFalse(RM.is_selected())
    
    def test_confirm_1(self): #5
        
        fulfill_1()
        origin = chrome.current_url
        
        confirm = chrome.find_element(By.NAME, "wish_num_submit")
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(confirm))
        confirm.submit()
        self.assertTrue(EC.url_to_be(origin))
        # wish_revoke untestable 'cause storageSession not involved.
        
    def test_continue_1(self): #6
        
        fulfill_1()
        origin = chrome.current_url
        
        conti = chrome.find_element(By.NAME, "pickup_date_submit")
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(conti))
        conti.submit()
        self.assertTrue(EC.url_changes(origin))
        
    def test_complete_11(self): #7
        
        fulfill_11()
        origin = chrome.current_url
    
        complete = chrome.find_element(By.NAME, "pickup_submit")
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(complete))
        complete.submit()
        self.assertTrue(EC.url_changes(origin))
        
    def test_cancel_submit_29(self): #8
        
        chrome.get(uri("29.html"))
        origin = chrome.current_url
        
        cancelpaths = listcancelpaths(datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=2))
        cancelpath = ""
        if len(cancelpaths) > 0:
            cancelpath += cancelpaths[0]
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        chrome.find_element(By.NAME, "cancelpath").send_keys(cancelpath)
        chrome.find_element(By.NAME, "cancel_submit").click()
        
        if cancelpath != "":
            self.assertTrue(EC.url_changes(origin))
        self.assertTrue(EC.url_to_be(origin))
        
    
# chrome.close() or chrome.quit()?

if __name__ == "__main__":
    
    unittest.main()
    
class Test_countdown(unittest.TestCase): # Tests self not working.

    def test_login_countdown_1(self): #
        
        chrome.get(uri("1.html")) # element only found static on layout.html
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.ID, 'logincountdown')))
        t0 = chrome.find_element(By.ID, 'logincountdown').text
        self.assertIn("Auto", t0) # js executed.
        sleep(4)
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(t0, chrome.find_element(By.ID, 'logincountdown').text)
        
    def test_countdown_2(self): # besides test, visibility problem does exist.
        
        chrome.get(uri("2.html"))
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'countdown')))
        t0 = chrome.find_element(By.CLASS_NAME, 'countdown').text
        self.assertNotEqual(t0, "") # js executed.
        sleep(4)
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(t0, chrome.find_element(By.CLASS_NAME, 'countdown').text)

class Test_text_change(unittest.TestCase): # Tests self not working. 
    
    def test_labels_1(self): #
        
        fulfill_1()
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="erase"]')))
        labeltext = chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]').text # found and got text.
        erase = chrome.find_element(By.CLASS_NAME, "erase") # found.
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of(erase))
        ac.move_to_element(erase).perform() # erase.onmouseover
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(labeltext, chrome.find_element(By.CSS_SELECTOR, 'label[for="erase"]').text) # or .get_attribute("innerHTML")
        
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="yesbox"]')))
        lt = chrome.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text                
        check = chrome.find_element(By.ID, "yes")
        WebDriverWait(chrome, 10, 0.5).until(EC.element_to_be_clickable(check))
        check.click()
        WebDriverWait(chrome, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(lt, chrome.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text)
                                    
    #def test_sign_11(self): #