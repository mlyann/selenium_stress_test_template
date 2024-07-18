import threading
from selenium import webdriver
from test import TestTest2  # Assuming your test class is defined in test_script.py
import concurrent.futures
import os

MeetingURL = "https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2696"

def run_test(instance_num):
    # Instantiate WebDriver for each thread
    driver = webdriver.Chrome()
    test_instance = TestTest2(driver,MeetingURL)
    try:
        test_instance.test_test2()
    finally:
        test_instance.teardown_method(None)
        driver.quit()
        print(f"Instance {instance_num} finished.")

def main(num_instances):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_instances) as executor:
        executor.map(run_test, range(num_instances))

if __name__ == "__main__":
    num_instances = 10  # Number of instances to run concurrently
    main(num_instances)
