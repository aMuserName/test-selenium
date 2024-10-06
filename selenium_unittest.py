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
import allure
from operator import itemgetter


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

    def publish_to_allure(self):
        #TODO: set dir
        csv_file = pandas.DataFrame(
                self.transactions[:-1],
                columns=self.transactions[-1])
        print(csv_file)
        allure.attach(
                csv_file,
                name='default',
                attachment_type=allure.attachment_type.CSV
        )

class CustomPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.calc = self._calculate()
        self.transactions = []

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
        return self.getText("span.error.ng-binding", "css_selector")

    def check_balance(self):
        return self.getText("//div[@class='center']//strong[2]", "xpath")

    def get_trans_history(self):

        # method of pressing button 
        trans = self.pressButton("btnClass1") 
        trans.click()
        time.sleep(2)
    
        table = self.getWebElement(".table.table-bordered.table-striped", "css_selector")
    
        raw_rows = table.find_elements(By.TAG_NAME,"tr")
        rows = []
        for row in raw_rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            _row = []
            for td in cells:
                _row.append(td.text)
            rows.append(_row)

        header = rows[0]
        rows = [[dt_convert(tmp[0])] + tmp[1:] + [dt_get(tmp[0])] for tmp in rows[1:]]
        rows = sorted(rows, key=itemgetter(-1))
        rows = [tmp[:-1] for tmp in rows] # del verbose elem
        rows.append(header)
        for line in rows:
            self.transactions.append(line)


class PythonSeleniumTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        service = Service()
        options = webdriver.ChromeOptions()
        #cls.driver = webdriver.Chrome(service = service, options = options)
        # TODO: set env 
        cls.driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                options=webdriver.ChromeOptions()
        )

    def test_process_page(self):
        delay = 10
        page = CustomPage(self.driver)
        page.launchWebPage("https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login", None)
        
        page.login()
        # TODO: assertion to successful login

        page.deposit()
        assert page.check_status() == 'Deposit Successful'
        # TODO: method to retrieve calc 
        assert page.check_balance() == page.calc
        time.sleep(14) # to sort rows later
        
        page.withdrawl()
        assert page.check_status() == 'Transaction successful'
        assert page.check_balance() == '0'
        time.sleep(2)    

        # GO TO TRANSACTIONS PAGE
        page.get_trans_history()
        assert page.transactions[0][1] == page.calc and page.transactions[0][2] == 'Credit' 
        assert page.transactions[1][1] == page.calc and page.transactions[1][2] == 'Debit' 

        page.publish_to_allure()

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
    res = datetime.strptime(from_dt, "%b %d, %Y %I:%M:%S %p")
    output = res.strftime(to_dt)
    return output

def dt_get(from_dt: str):
    return datetime.strptime(from_dt, "%b %d, %Y %I:%M:%S %p")

if __name__ == '__main__':
    unittest.main()
