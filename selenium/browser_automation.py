from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class BrowserAutomation:
    def __init__(self, driver, meeting_url):
        self.driver = driver
        self.MeetingURL = meeting_url

    def open_new_tabs(self, n):
        for _ in range(n):
            # Open a new tab using JavaScript
            self.driver.execute_script("window.open('');")
            
            # Switch to the new tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            
            # Navigate to the meeting URL in the new tab
            self.driver.get(self.MeetingURL)
            time.sleep(1)


