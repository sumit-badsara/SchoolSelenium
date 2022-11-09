from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# start chrome instance with remote debugging enabled
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome("/Users/raghav/Documents/chromedriver", options=chrome_options)

# get the url 
driver.get("https://src.udiseplus.gov.in/newSearchSchool/searchSchool")

# print chrome session id, url
print(driver.command_executor._url)
print(driver.session_id)
while True:
    pass
    time.sleep(1)
