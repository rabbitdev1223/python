import pandas as pd
import time
import os
import datetime as dt1
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select

curr_dir=os.getcwd()
options = Options()
options.add_experimental_option("prefs", {
  "download.default_directory": curr_dir,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})

# api="api.spreaker.com"
# endpoint="/v2/shows/3292827/statistics/plays?c=en_US&from=2021-01-01&to=2021-10-17&group=month"
# url = "https://"+api+endpoint

# 1 min, I need to make a small change...
# Not working, have to fix this


driver = webdriver.Chrome(executable_path=curr_dir+"\\chromedriver.exe",options=options)
url="https://www.spreaker.com/"
url_login="https://www.spreaker.com/login?redirect=%2F"
stats_login="https://www.spreaker.com/cms/statistics"
username="matthendricks87@gmail.com"
passw="Test@123"
driver.get (url_login)
driver.find_element_by_id("identity").send_keys(username)
driver.find_element_by_id ("password").send_keys(passw)
driver.find_element_by_id("login-form-submit").click()
driver.get (stats_login)


# Either Select Custom and then Change the from date to Jan 01, 2021 or directly try to change the from date 
dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page_main"]/div[2]/div/div/div/section[2]/div[1]/div/div[1]/select')))
# driver.find_element_by_xpath('//div[@class="form_field form_field_"]').click()
period = WebDriverWait(driver, 10).until(lambda driver:Select(dropdown))
#period=Select(dropdown)
for op in period.options:
    print(op.text, op.get_attribute('value')) 

time.sleep(4)
# period.select_by_visible_text("Custom")
period.select_by_value("custom")
time.sleep(4)

# Trying to pass date in the From field
datefield = driver.find_element_by_xpath('//*[@id="page_main"]/div[2]/div/div/div/section[2]/div[1]/div/div[2]/button[1]')
ActionChains(driver).move_to_element(datefield).click().send_keys('01/01/2021').perform()

