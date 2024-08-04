import threading
from selenium import webdriver
from test_script import TestTest2  # Assuming your test class is defined in test_script.py
import concurrent.futures
import os
import time

MeetingURL = "https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2711"

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

def main(num_instances, interval = 2):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_instances) as executor:
        for instance_num in range(num_instances):
            executor.submit(run_test, instance_num)
            time.sleep(interval)  # Wait for `interval` seconds before starting the next instance

if __name__ == "__main__":
    num_instances = 30 # Number of instances to run concurrently
    main(num_instances)
