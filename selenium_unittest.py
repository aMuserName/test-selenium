from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pandas

def fibonacci_of(n):
    # Validate the value of n
    if not (isinstance(n, int) and n >= 0):
        raise ValueError(f'Positive integer number expected, got "{n}"')


    # Handle the base cases
    if n in {0, 1}:
        return n


    previous, fib_number = 0, 1
    for _ in range(2, n + 1):
        # Compute the next Fibonacci number, remember the previous one
        previous, fib_number = fib_number, previous + fib_number

    return previous

def dt_convert(from_dt: str, to_dt: str = "%d %B %Y %H:%M:%S"):
    print(from_dt)
    res = datetime.strptime(from_dt, "%b %d, %Y %I:%M:%S %p")
    output = res.strftime(to_dt)
    return output

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
    
    # method of pressing button
    buts = driver.find_elements(By.CSS_SELECTOR,".btn.btn-lg.tab")
    for each in buts:
        if "btnClass2" == each.get_dom_attribute("ng-class"):
            deposit = each 
        print(each.get_dom_attribute("ng-class"))

    deposit.click()
    time.sleep(2)
    
    input_deposit = driver.find_element(By.XPATH, "//input[@type='number']")
    print(buts) 
    print(input_deposit)
    
    input_deposit.clear()
    _today = datetime.today().day + 1
    calc = fibonacci_of(_today)
    print(_today, calc)
    input_deposit.send_keys(str(calc))    
    time.sleep(2)

    deposit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    print(deposit_btn)
    
    deposit_btn.click()
    time.sleep(2)
    
    label = driver.find_element(By.CSS_SELECTOR,"span.error.ng-binding")
    assert label.text == 'Deposit Successful'
    time.sleep(2)

    ## test
    print("Here goes")
    general_bar = driver.find_elements(By.XPATH, "//div[@class='center']//strong[2]")
    print(general_bar)
    print(general_bar[0].text)
    ## test


    # method of pressing button
    buts = driver.find_elements(By.CSS_SELECTOR,".btn.btn-lg.tab")
    for each in buts:
        if "btnClass3" == each.get_dom_attribute("ng-class"):
            deposit = each 
        print(each.get_dom_attribute("ng-class"))

    deposit.click()
    time.sleep(2)

    # repeating code below
    input_deposit = driver.find_element(By.XPATH, "//input[@type='number']")
    print(buts) 
    print(input_deposit)
    
    input_deposit.clear()
    time.sleep(2)
    input_deposit.send_keys(str(calc))    
    time.sleep(2)

    deposit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    print(deposit_btn)
    
    deposit_btn.click()
    time.sleep(2)

    balance = driver.find_element(By.XPATH, "//div[@class='center']//strong[2]")
    assert balance.text == '0'
    
    # GO TO TRANSACTIONS PAGE

    # method of pressing button
    buts = driver.find_elements(By.CSS_SELECTOR,".btn.btn-lg.tab")
    for each in buts:
        if "btnClass1" == each.get_dom_attribute("ng-class"):
            deposit = each 
        print(each.get_dom_attribute("ng-class"))

    deposit.click()
    time.sleep(2)

    table = driver.find_element(By.CSS_SELECTOR,".table.table-bordered.table-striped")

    raw_rows = table.find_elements(By.TAG_NAME, "tr")
    rows = []
    for row in raw_rows:
        print(row)
        cells = row.find_elements(By.TAG_NAME, 'td')
        _row = []
        for td in cells:
            _row.append(td.text)
            print(td.text, end=' ')
        rows.append(_row)
        print(end='\n')
    header = rows[0]
    rows = [[dt_convert(tmp[0])] + tmp[1:] for tmp in rows[1:]]
    print(rows)

    df = pandas.DataFrame(rows, columns=header)
    print(df)
    #deposit_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".btn.btn-default"))).click()
finally:
    driver.quit()

