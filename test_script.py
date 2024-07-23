import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random_number
import browser_automation
import os

class TestTest2():
    def __init__(self, driver,MeetingURL):
        self.driver = driver
        self.vars = {}
        self.MeetingURL = MeetingURL
    
    def teardown_method(self, method):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    
    def wait_for_window(self, timeout=2):
        time.sleep(timeout / 1000)
        wh_now = self.driver.window_handles
        wh_then = self.vars.get("window_handles", [])
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()
    
    def test_test2(self):
        try:
            # 1 | open | https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2685 | 
            self.driver.get(self.MeetingURL)
            time.sleep(30)
            # 2 | setWindowSize | 1620x1010 | 
            self.driver.set_window_size(1620, 1010)
            time.sleep(30)
            # 3 | click | id=btnToSignin | 
            self.driver.find_element(By.ID, "btnToSignin").click()
            time.sleep(30)
            # time.sleep(5)
            # 4 | click | id=select2-ddlUnit-container | 
            self.driver.find_element(By.ID, "select2-ddlUnit-container").click()
            time.sleep(30)
            # 5 | click | css=.select2-search__field | 
            # 6 | type | css=.select2-search__field | 100
            self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(random_number.select_random_number())
            time.sleep(30)
            # 7 | sendKeys | css=.select2-search__field | ${KEY_ENTER}
            self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(Keys.ENTER)
            time.sleep(30)
            # 8 | click | id=btnPE1 | 
            self.driver.find_element(By.ID, "btnPE1").click()
            time.sleep(30)
            # 9 | click | id=txtVerCode | 
            self.driver.find_element(By.ID, "txtVerCode").click()
            time.sleep(30)
            # 10 | type | id=txtVerCode | 112233
            self.driver.find_element(By.ID, "txtVerCode").send_keys("112233")
            time.sleep(30)
            # 11 | click | id=btnP1 | 
            self.driver.find_element(By.ID, "btnP1").click()
            time.sleep(30)
            # 12 | click | css=.btn_SinedInNormal | 
            self.driver.find_element(By.CSS_SELECTOR, ".btn_SinedInNormal").click()
            time.sleep(30)
            
            # # Initialize the BrowserAutomation with the driver and meeting URL
            # automation = newTab.BrowserAutomation(self.driver, self.MeetingURL)

            # # Open 5 new tabs
            # automation.open_new_tabs(9)


            time.sleep(900)

                
        except Exception as e:
            print("------------------------------------------------------------------")
            print(f"Exception occurred: {str(e)}")
            print("------------------------------------------------------------------")
            raise e
