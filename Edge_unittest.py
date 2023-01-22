# selenium. No sessionStorage involved. Nor db.
import unittest
import os
import pathlib 
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait # Important to wait for the web to run. Or: 
from time import sleep # only if there's no applicable EC for WebDriverWait.

def uri(filename):        
    return pathlib.Path(os.path.abspath("templates")).as_uri() + f"/{filename}"

driver = webdriver.Edge(EdgeChromiumDriverManager().install())
ac = ActionChains(driver)

# browser name = driver.name
# html = driver.page_source
# next page = driver.forward()
# page title = driver.title

# Use "inspect" to locate elements. "view source" returns only static source code without js execution.

def fulfill_1(): # fulfill all inputs in 1.html without Key.Enter

    driver.get(uri("1.html"))
    
    # pickup_date
    WebDriverWait(driver, 10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_date"), is_selected=False)) # found untouched.
    Select(driver.find_element(By.ID, "pickup_date")).select_by_index(1) # or str "1". 0: explanation. Or: Select(date).select_by_value(). Select(date).select_by_visible_text("")
    WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_selected(driver.find_elements(By.TAG_NAME, "option")[1]))
    # Unnecessary: self.assertIn("today", date.get_attribute("value")) # value != .text(html code)
    
    # now_num
    num = driver.find_element(By.ID, "now_num")
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(num)) # found and seen.
    num.send_keys("1") # > 0, <= product inventory. Others: num.submit(). num.clear()
    WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "now_num"), "1"))    
    
    # wish_num
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "wish_num")))
    driver.find_element(By.ID, "wish_num").send_keys(2)
    WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "wish_num"), "2"))

    # fix wish_num. as default if session involved.
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "yes")))
    check = driver.find_element(By.ID, "yes")
    WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(check))
    check.click() # check.checked = true; 
    js = """
    const check = document.querySelector('#yes'); 
    check.setAttribute('disabled', 'disabled'); 
    document.querySelector('body > div > form > label:nth-child(4)').innerHTML = 'Fixed';
    """
    driver.execute_script(js)

def fulfill_11(): # fulfill all inputs in 11.html without Key.Enter

    driver.get(uri("11.html"))
        
    WebDriverWait(driver, 10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_time"), is_selected=False)) # found untouched.
    Select(driver.find_element(By.ID, "pickup_time")).select_by_index(1) # 0: explanation.
    WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_selected(driver.find_elements(By.TAG_NAME, "option")[1]))
        
    contact = driver.find_element(By.ID, "contact")
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(contact))
    contact.send_keys("contact")
    WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "contact"), "contact"))
        
    phone = driver.find_element(By.ID, "phone")
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(phone))
    phone.send_keys("phone numbers")
    WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "phone"), "phone numbers"))
        
    title = driver.find_element(By.ID, "title")
    WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(title))
    title.send_keys("title surname")
    WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "title"), "title surname"))
    
class NO_sessionStorage_involved(unittest.TestCase):
    
    def test_1(self): #1 and also 1.html
        
        fulfill_1()       
        driver.refresh() # Elements must be reread.
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertIn("?", driver.find_element(By.ID, "pickup_date").get_attribute("value")) # Default: "Preferred...?"
        self.assertEqual(driver.find_element(By.ID, "now_num").get_attribute("value"), "") 
        #Or: self.assertTrue(EC.text_to_be_present_in_element_attribute((By.ID, "now_num"), "value", ""))
        #Or: self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "now_num"), ""))

class Test_button_click(unittest.TestCase):

    def test_back_button_11(self): #2        
        
        driver.get(uri("11.html"))
        
        origin = driver.current_url
        back = driver.find_element(By.ID, "back")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(back)) # found working. Otherwise click() can fail.
        back.click()
        self.assertTrue(EC.url_changes(origin)) # Or: self.assertNotEqual(origin, driver.current_url)
        driver.back()
        self.assertTrue(EC.url_to_be(origin)) # Or: self.assertEqual(origin, driver.current_url)

    def test_erase_button_1(self): #3
        
        fulfill_1()
        
        erase = driver.find_element(By.CLASS_NAME, "erase") # or By.NAME
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(erase)) # found working.
        erase.click() # Or: ac.click(erase).perform(), execute_script, erase.send_keys(Keys.ENTER)
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "now_num"), "")) # self.assertEqual(date.get_attribute("value"), "")
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "pickup_date"), "")) # self.assertEqual(num.get_attribute("value"), "")

    def test_erase_button_11(self): #4
        
        fulfill_11()
        
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "RememberMe")))
        RM = driver.find_element(By.ID, "RememberMe")
        # during key in title etc.: self.assertTrue(EC.element_to_be_clickable(RM)).
        # Otherwise:
        #self.assertTrue(RM.is_selected()) 
        #self.assertFalse(RM.is_enabled())
        
        erase = driver.find_element(By.CLASS_NAME, "erase") # or By.NAME
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(erase))
        
        erase.click()
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "pickup_time"), ""))
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "contact"), ""))    
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "phone"), ""))
        self.assertTrue(EC.text_to_be_present_in_element_value((By.ID, "title"), ""))
        self.assertTrue(RM.is_enabled())
        self.assertFalse(RM.is_selected())
    
    def test_confirm_1(self): #5
        
        fulfill_1()
        origin = driver.current_url
        
        confirm = driver.find_element(By.NAME, "wish_num_submit")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(confirm))
        confirm.submit()
        self.assertTrue(EC.url_to_be(origin))
        # wish_revoke untestable 'cause storageSession not involved.
        
    def test_continue_1(self): #6
        
        fulfill_1()
        origin = driver.current_url
        
        conti = driver.find_element(By.NAME, "pickup_date_submit")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(conti))
        conti.submit()
        self.assertTrue(EC.url_changes(origin))
        
    def test_complete_11(self): #7
        
        fulfill_11()
        origin = driver.current_url
    
        complete = driver.find_element(By.NAME, "pickup_submit")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(complete))
        complete.submit()
        self.assertTrue(EC.url_changes(origin))
        
    def test_cancel_submit_29(self): #8
        
        tests = ['', 'test']
        
        for cp in tests:
            driver.get(uri("29.html"))
            origin = driver.current_url
            WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
            driver.find_element(By.NAME, "cancelpath").send_keys(cp)
            WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.NAME, "cancelpath"), cp))
            driver.find_element(By.NAME, "cancel_submit").click()
            if cp == '':
                self.assertTrue(EC.url_to_be(origin))
            self.assertTrue(EC.url_changes(origin))

class Test_text_change_js(unittest.TestCase): # not redundant at all?!

    def test_1(self): #9
        
        fulfill_1()

        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > label')))
        labeltext = driver.find_element(By.CSS_SELECTOR, 'body > label').text # found and got text.
        erase = driver.find_element(By.CLASS_NAME, "erase") # found.
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(erase))
        
        js_onmouseover = """
        document.querySelector('.erase').onmouseover = () => { 
        document.querySelector('body > label').innerHTML = 
        'Recommended on public or shared devices.'}
        """
        driver.execute_script(js_onmouseover)
        ac.move_to_element(erase).perform() # erase.onmouseover
        sleep(1)
        self.assertNotEqual(labeltext, driver.find_element(By.CSS_SELECTOR, 'body > label').text) # or .get_attribute("innerHTML")

        js_onmouseout = js_onmouseover.replace("onmouseover", "onmouseout").replace("Recommended on public or shared devices.", "all input.")
        driver.execute_script(js_onmouseout)
        ac.move_by_offset(0, erase.size['height']).perform() # vaguely like erase.onmouseout
        sleep(1)
        self.assertEqual(labeltext, driver.find_element(By.CSS_SELECTOR, 'body > label').text) # or .get_attribute("innerHTML")

        wish_num = driver.find_element(By.ID, "wish_num")
        wish_num.clear()
        wish_num.send_keys(1)
        WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "wish_num"), "1"))
        js_enable_check = """
        const check = document.querySelector('#yes'); 
        check.removeAttribute('disabled'); 
        document.querySelector('body > div > form > label:nth-child(4)').innerHTML = 'Fix number on this device.';
        """
        driver.execute_script(js_enable_check)
        
        WebDriverWait(driver, 10, 0.5).until(EC.text_to_be_present_in_element_attribute((By.CSS_SELECTOR, 'label[for="yesbox"]'), 'innerHTML', 'Fix number on this device.'))
        lt = driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text # 'Fix number on this device.'
        
        check = driver.find_element(By.ID, "yes")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(check))
        check.click()
        js_disable_check = """
        const check = document.querySelector('#yes'); 
        check.setAttribute('disabled', 'disabled'); 
        document.querySelector('body > div > form > label:nth-child(4)').innerHTML = 'Fixed';
        """
        driver.execute_script(js_disable_check)
        self.assertFalse(check.is_enabled())
        self.assertNotEqual(lt, driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text)

class Test_timing_js(unittest.TestCase): # works here, but not there?

    def test_2_and_3(self): #10

        js = """
        let countdown = 60;
        setInterval(() => {
        countdown -= 1;
        document.querySelector('.countdown').innerHTML = 
        `Redirect after ${countdown} seconds`;
        if (countdown == -1) { location.href = '/loggingin';}
        }, 1000);
        """

        for ele in ["2", "3"]:

            driver.get(uri(ele + ".html"))
            # if ele == "2": self.assertFalse(driver.find_element(By.CSS_SELECTOR, "header > h2").is_displayed()) # not there. 'cause of extension.
            driver.execute_script(js)
            WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, "countdown")))
            t1 = driver.find_element(By.CLASS_NAME, "countdown").text
            sleep(2)
            self.assertNotEqual(t1, driver.find_element(By.CLASS_NAME, "countdown").text)

    def test_1_and_11_extends_layout(self): #11

        js = """
        let n = 300;
        setInterval(() => {
        n -= 1;
        document.querySelector('#logincountdown').innerHTML = 
        `Auto Logout after ${n} seconds.`;
        if (n == -1) { location.href = "/";}
        }, 1000);
        """

        driver.get(uri("layout.html"))
        driver.execute_script(js)
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "logincountdown")))
        t1 = driver.find_element(By.ID, "logincountdown").text
        sleep(2)
        self.assertNotEqual(t1, driver.find_element(By.ID, "logincountdown").text)

if __name__ == "__main__":

    unittest.main()

    def test_1_and_11(self): # works there, but not here. 'cause of extension.

        js = """
        let n = 300;
        setInterval(() => {
        n -= 1;
        document.querySelector('#logincountdown').innerHTML = 
        `Auto Logout after ${n} seconds.`;
        if (n == -1) { location.href = "/";}
        }, 1000);
        """

        for ele in ["1", "11"]:

            driver.get(uri(ele + ".html"))
            driver.execute_script(js)
            WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, "logincountdown")))
            t1 = driver.find_element(By.ID, "logincountdown").text
            sleep(2)
            self.assertNotEqual(t1, driver.find_element(By.ID, "logincountdown").text)        

class Test_text_change(unittest.TestCase): # Tests self not working. 
    
    def test_labels_1(self): #
        
        fulfill_1()

        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'body > label')))
        labeltext = driver.find_element(By.CSS_SELECTOR, 'body > label').text # found and got text.
        erase = driver.find_element(By.CLASS_NAME, "erase") # found.
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of(erase))
        ac.move_to_element(erase).perform() # erase.onmouseover
        sleep(5)
        self.assertNotEqual(labeltext, driver.find_element(By.CSS_SELECTOR, 'body > label').text) # or .get_attribute("innerHTML")
        
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="yesbox"]')))
        lt = driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text                
        check = driver.find_element(By.ID, "yes")
        WebDriverWait(driver, 10, 0.5).until(EC.element_to_be_clickable(check))
        check.click()
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(lt, driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text)
    
class Test_countdown(unittest.TestCase): # Tests self not working.

    def test_login_countdown_1(self): #
        
        driver.get(uri("1.html")) # element only found static on layout.html
        
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.ID, 'logincountdown')))
        t0 = driver.find_element(By.ID, 'logincountdown').text
        self.assertIn("Auto", t0) # js executed.
        sleep(4)
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(t0, driver.find_element(By.ID, 'logincountdown').text)
        
    def test_countdown_2(self):
        
        driver.get(uri("2.html"))
        
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'countdown')))
        t0 = driver.find_element(By.CLASS_NAME, 'countdown').text
        self.assertNotEqual(t0, "") # js executed.
        sleep(4)
        WebDriverWait(driver, 10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        self.assertNotEqual(t0, driver.find_element(By.CLASS_NAME, 'countdown').text)
                                    
    #def test_sign_11(self): #
