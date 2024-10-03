from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options = options)
driver.get("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login")
print(driver.title)
try:
    delay = 10
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-primary.btn-lg"))).click()
    import time
    time.sleep(2)

    select = Select(WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'userSelect'))))
    select.select_by_value('2') # Harry Potter  
    time.sleep(2)

    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-default"))).click()
    time.sleep(2)

    buts = driver.find_elements(By.CSS_SELECTOR,".btn.btn-lg.tab")
    for each in buts:
        if "btnClass2" == each.get_dom_attribute("ng-class"):
            deposit = each 
        print(each.get_dom_attribute("ng-class"))

    deposit.click()
    time.sleep(2)
    
    input_deposit = driver.find_element(By.XPATH, "//input[@type='number']")
    print(buts) 
    #input_deposit = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 
   #     "input.form-control.ng-dirty.ng-valid-number.ng-invalid.ng-invalid-required.ng-touched"))).click()

    print(input_deposit)
#    input_deposit.click()
    input_deposit.clear()
    input_deposit.send_keys("1234")
    
    time.sleep(2)
    #"form-control.ng-dirty.ng-valid-number.ng-invalid.ng-invalid-required.ng-touched"
finally:
    driver.quit()


