# No unittest version for testing various browsers all at once: Chrome, Firefox, Edge, Ie. No Opera.
# If this passed, no further selenium tests needed.
# selenium. No sessionStorage involved. Nor db.

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException as wde
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait # Important to wait for the web to run. Or: 
from time import sleep # only if there's no applicable EC for WebDriverWait.
from uri_html import uri

l = ['Chrome', 'Firefox', 'Edge', 'IE']

def browser_check():
    
    try:
        webdriver.Chrome()
    except:
        l.remove('Chrome')
        print("No Chrome working.")
    
    try:
        webdriver.Firefox()
    except:
        l.remove('Firefox')
        print("No Firefox working.")
        
    try:
        webdriver.Edge()
    except:
        l.remove('Edge')
        print("No Edge working.")

    try:
        webdriver.Ie()
    except:
        l.remove('IE')
        print("No Ie working.")

def test(driver): # drivers left to be assigned in "__main__".
    
    NO_sessionStorage_involved() #1
    test_back_button_11() #2
    test_erase_button_1() #3
    test_erase_button_11() #4
    test_confirm_1() #5
    test_continue_1() #6
    test_complete_11() #7
    test_cancel_submit_29() #8
    #test_login_countdown_1()
    #test_countdown_2()
    #test_labels_1()

# Test process begin:

# browser name = driver.name
# html = driver.page_source
# next page = driver.forward()
# page title = driver.title
# driver.close(): close the current page. 
# driver.quit(): quit the whole browser.
# Use "inspect" to locate elements. "view source" returns only static source code without js execution.

def fulfill_1(): # fulfill all inputs in 1.html without Key.Enter

    driver.get(uri("1.html"))
    
    # pickup_date
    WebDriverWait(driver,  10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_date"), is_selected=False)) # found untouched.
    Select(driver.find_element(By.ID, "pickup_date")).select_by_index(1) # or str "1". 0: explanation. Or: Select(date).select_by_value(). Select(date).select_by_visible_text("")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_selected(driver.find_elements(By.TAG_NAME, "option")[1]))
    # Unnecessary: driver.assertIn("today", date.get_attribute("value")) # value != .text(html code)
    
    # now_num
    num = driver.find_element(By.ID, "now_num")
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of(num)) # found and seen.
    num.send_keys("1") # > 0, <= product inventory. Others: num.submit(). num.clear()
    WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "now_num"), "1"))    
    
    # wish_num
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.ID, "wish_num")))
    driver.find_element(By.ID, "wish_num").send_keys(2)
    WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "wish_num"), "2"))

def fulfill_11(): # fulfill all inputs in 11.html without Key.Enter

    driver.get(uri("11.html"))
        
    WebDriverWait(driver,  10, 0.5).until(EC.element_located_selection_state_to_be((By.ID, "pickup_time"), is_selected=False)) # found untouched.
    Select(driver.find_element(By.ID, "pickup_time")).select_by_index(1) # 0: explanation.
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_selected(driver.find_elements(By.TAG_NAME, "option")[1]))
        
    contact = driver.find_element(By.ID, "contact")
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of(contact))
    contact.send_keys("contact")
    WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "contact"), "contact"))
        
    phone = driver.find_element(By.ID, "phone")
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of(phone))
    phone.send_keys("phone numbers")
    WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "phone"), "phone numbers"))
        
    title = driver.find_element(By.ID, "title")
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of(title))
    title.send_keys("title surname")
    WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.ID, "title"), "title surname"))
        
def NO_sessionStorage_involved(): #1 and also 1.html
        
    fulfill_1()       
    driver.refresh() # Elements must be reread.
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
    assert "?" in driver.find_element(By.ID, "pickup_date").get_attribute("value")
    assert EC.text_to_be_present_in_element_value((By.ID, "now_num"), "")

def test_back_button_11(): #2
        
    driver.get(uri("11.html"))
    origin = driver.current_url
    back = driver.find_element(By.ID, "back")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(back)) # found working. Otherwise click() can fail.
    back.click()
    assert EC.url_changes(origin)
    driver.back()
    assert EC.url_to_be(origin)

def test_erase_button_1(): #3
        
    fulfill_1()
        
    erase = driver.find_element(By.CLASS_NAME, "erase") # or By.NAME
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(erase)) # found working.
    erase.click() # Or: ActionChains(driver).click(erase).perform(), execute_script, erase.send_keys(Keys.ENTER)
    assert EC.text_to_be_present_in_element_value((By.ID, "now_num"), "")
    assert EC.text_to_be_present_in_element_value((By.ID, "pickup_date"), "")
        
def test_erase_button_11(): #4
        
    fulfill_11()
        
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.ID, "RememberMe")))
    RM = driver.find_element(By.ID, "RememberMe")
    # during key in title etc.: driver.assertTrue(EC.element_to_be_clickable(RM)).
    # Otherwise:
    #driver.assertTrue(RM.is_selected()) 
    #driver.assertFalse(RM.is_enabled())
        
    erase = driver.find_element(By.CLASS_NAME, "erase") # or By.NAME
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(erase))
    erase.click()

    assert EC.text_to_be_present_in_element_value((By.ID, "pickup_time"), "") 
    assert EC.text_to_be_present_in_element_value((By.ID, "contact"), "") 
    assert EC.text_to_be_present_in_element_value((By.ID, "phone"), "") 
    assert EC.text_to_be_present_in_element_value((By.ID, "title"), "") 
    assert RM.is_enabled() 
    assert not RM.is_selected()
    
def test_confirm_1(): #5
        
    fulfill_1()
    origin = driver.current_url
        
    confirm = driver.find_element(By.NAME, "wish_num_submit")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(confirm))
    confirm.submit()
    assert EC.url_to_be(origin)
    # wish_revoke untestable 'cause storageSession not involved.
        
def test_continue_1(): #6
        
    fulfill_1()
    origin = driver.current_url
        
    conti = driver.find_element(By.NAME, "pickup_date_submit")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(conti))
    conti.submit()
    assert EC.url_changes(origin)
        
def test_complete_11(): #7
        
    fulfill_11()
    origin = driver.current_url
    
    complete = driver.find_element(By.NAME, "pickup_submit")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(complete))
    complete.submit()
    assert EC.url_changes(origin)
        
def test_cancel_submit_29(): #8
        
    tests = ['', 'test']

    for cp in tests:
        driver.get(uri("29.html"))
        origin = driver.current_url
        WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
        driver.find_element(By.NAME, "cancelpath").send_keys(cp)
        WebDriverWait(driver,  10, 0.5).until(EC.text_to_be_present_in_element_value((By.NAME, "cancelpath"), cp))
        driver.find_element(By.NAME, "cancel_submit").click()
        if cp == '':
            assert EC.url_to_be(origin)
        assert EC.url_changes(origin)

def test_login_countdown_1(): # The followings not quite working as test self.
        
    driver.get(uri("1.html")) # element only found static on layout.html
        
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.ID, 'logincountdown')))
    t0 = driver.find_element(By.ID, 'logincountdown').text
    assert "Auto" in t0 # js executed.
    sleep(4)
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
    assert t0 != driver.find_element(By.ID, 'logincountdown').text
        
def test_countdown_2(): # besides test problem, visibility problem does exist.
        
    driver.get(uri("2.html"))
        
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'countdown')))
    t0 = driver.find_element(By.CLASS_NAME, 'countdown').text
    assert t0 != "" # js executed.
    sleep(4)
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
    assert t0 != driver.find_element(By.CLASS_NAME, 'countdown').text

def test_labels_1(): #
        
    fulfill_1()
        
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="erase"]')))
    labeltext = driver.find_element(By.CSS_SELECTOR, 'label[for="erase"]').text # found and got text.
    erase = driver.find_element(By.CLASS_NAME, "erase") # found.
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of(erase))
    ActionChains(driver).move_to_element(erase).perform() # erase.onmouseover
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
    assert labeltext != driver.find_element(By.CSS_SELECTOR, 'label[for="erase"]').text # or .get_attribute("innerHTML")
        
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[for="yesbox"]')))
    lt = driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text                
    check = driver.find_element(By.ID, "yes")
    WebDriverWait(driver,  10, 0.5).until(EC.element_to_be_clickable(check))
    check.click()
    WebDriverWait(driver,  10, 0.5).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "html")))
    assert lt != driver.find_element(By.CSS_SELECTOR, 'label[for="yesbox"]').text
                                    
#def test_sign_11(): #

if __name__ == '__main__': # Running without variable in def() must imply "driver" being explicitly appointed here.
    
    browser_check() # [str, str...]
    print("Checking browsers: " + ', '.join(l))
    
    for ele in l:
        
        if ele == "Chrome":
            driver = webdriver.Chrome()
            test(driver)
            print("Chrome checked.")
            
        if ele == "Firefox":
            driver = webdriver.Firefox()
            test(driver)
            print("Firefox checked.")
        
        if ele == "Edge":
            driver = webdriver.Edge()
            test(driver)
            print("Edge checked.")

        if ele == "IE":
            driver = webdriver.Ie()
            test(driver)
            print("IE checked.")