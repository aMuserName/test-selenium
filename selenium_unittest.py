from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service = service, options = options)
driver.get("https://github.com")
print(driver.title)
assert "GitHub" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.send_keys("testname")
elem.send_keys(Keys.RETURN)
assert "Not results found." not in driver.page_source
driver.close()
