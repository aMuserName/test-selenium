from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pandas
import unittest
import time


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def launchWebPage(self, url, title):
        try:
            self.driver.get(url)
            # assert title in self.driver.title
        except:
            print(f'Failed to load page: {url}')

    def getLocatorType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == 'id':
            return By.ID
        elif locatorType == 'css_selector':
            return By.CSS_SELECTOR
        elif locatorType == 'xpath':
            return By.XPATH
        else:
            print(f"Locator type not found {locatorType}")

    def waitForElement(self, locatorValue, locatorType='id'):
        webElement = None
        delay = 25
        try:
            locatorType = locatorType.lower()
            locatorByType = self.getLocatorType(locatorType)
            wait = WebDriverWait(self.driver, delay, poll_frequency=1,
                    ignored_exceptions=[ElementNotVisibleException, NoSuchElementException])
            webElement = wait.until(EC.presence_of_element_located((locatorByType, locatorValue)))
        except:
            print(f"Waiting failed for element {locatorValue} by {locatorType}")
        return webElement

    def getWebElement(self, locatorValue, locatorType='id'):
        webElement = None
        try:
            locatorType = locatorType.lower()
            locatorByType = self.getLocatorType(locatorType)
            webElement = self.driver.find_element(locatorByType, locatorValue)
        except:
            print(f"Failed to find element {locatorValue} by {locatorType}")
        return webElement

    def getWebElements(self, locatorValue, locatorType='id'):
        webElements = None
        try:
            locatorType = locatorType.lower()
            locatorByType = self.getLocatorType(locatorType)
            webElements = self.driver.find_elements(locatorByType, locatorValue)
        except:
            print(f"Failed to find elements {locatorValue} by {locatorType}")
        return webElements

    def clickOnElement(self, locatorValue, locatorType):
        webElement = None
        try:
            locatorType = locatorType.lower()
            webElement = self.waitForElement(locatorValue, locatorType)
            webElement.click()
        except:
            print(f"Failed to click on element {locatorValue} by {locatorType}")
        return False

    def sendText(self, text, locatorValue, locatorType='id'):
        try:
            locatorType = locatorType.lower()
            webElement = self.waitForElement(locatorValue, locatorType)
            webElement.send_keys(text)
        except:
            print(f"Failed to send text to element {locatorValue} by {locatorType}")
        return False

    def clearText(self, locatorValue, locatorType='id'):
        try:
            locatorType = locatorType.lower()
            webElement = self.waitForElement(locatorValue, locatorType)
            webElement.clear()
        except:
            print(f"Failed to clear input of element {locatorValue} by {locatorType}")
        return False

    def getText(self, locatorValue, locatorType='id'):
        elementText = None
        try:
            locatorType = locatorType.lower()
            webElement = self.waitForElement(locatorValue, locatorType)
            elementText = webElement.text
        except:
            print(f"Failed to get text of element {locatorValue} by {locatorType}")

        return elementText

class CustomPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.calc = self._calculate()

    def pressButton(self, class_value, class_type="ng-class"):
        # TODO: refactor
        buts = self.getWebElements(".btn.btn-lg.tab", "css_selector")
        for each in buts:
            if class_value == each.get_dom_attribute(class_type):
                button = each 
        return button

    def login(self, user='2'):
        self.clickOnElement(".btn.btn-primary.btn-lg", "css_selector")
        time.sleep(2)
        select = Select(self.getWebElement('userSelect', "id"))
        select.select_by_value(user) # Harry Potter  
        time.sleep(2)

        self.clickOnElement(".btn.btn-default", "css_selector")
        time.sleep(2)

    def deposit(self):
        # method of pressing buttoni
        # TODO: chained path
        
        deposit = self.pressButton("btnClass2") 
        deposit.click()
        time.sleep(2)
        print(self.calc) 
        self.clearText("//input[@type='number']", "xpath")
        time.sleep(2)
        
        self.sendText(self.calc, "//input[@type='number']", "xpath")
        time.sleep(2)

        self.clickOnElement("//button[@type='submit']", "xpath")
        time.sleep(2)

    def withdrawl(self):
        # method of pressing button 
        withdrawl = self.pressButton("btnClass3") 
        withdrawl.click()
        time.sleep(2)
       
        self.clearText("//input[@type='number']", "xpath")
        time.sleep(2)

        self.sendText(self.calc, "//input[@type='number']", "xpath")
        time.sleep(2)

        self.clickOnElement("//button[@type='submit']", "xpath")
        time.sleep(2)    

    def _calculate(self):
        _today = datetime.today().day + 1
        calc = fibonacci_of(_today)
        return str(calc)

    def check_status(self):
        raise NotImplementedError()

    def check_balance(self):
        raise NotImplementedError()

    def get_trans_history(self):
        raise NotImplementedError()

class PythonSeleniumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        service = Service()
        options = webdriver.ChromeOptions()
        cls.driver = webdriver.Chrome(service = service, options = options)

    def test_process_page(self):
        delay = 10
        page = CustomPage(self.driver)
        page.launchWebPage("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login", None)
        
        page.login()
        
        page.deposit()
        label = page.getText("span.error.ng-binding", "css_selector")
        assert label == 'Deposit Successful'
        time.sleep(2)
        
        page.withdrawl()
        label = page.getText("span.error.ng-binding", "css_selector")
        assert label == 'Transaction successful'
        time.sleep(2)
            
        balance = page.getText("//div[@class='center']//strong[2]", "xpath")
        assert balance == '0'

        # GO TO TRANSACTIONS PAGE

        # method of pressing button 
        trans = page.pressButton("btnClass1") 
        trans.click()
        time.sleep(2)
    

        table = page.getWebElement(".table.table-bordered.table-striped", "css_selector")
    
        raw_rows = table.find_elements(By.TAG_NAME,"tr")
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

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


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


if __name__ == '__main__':
    unittest.main()
