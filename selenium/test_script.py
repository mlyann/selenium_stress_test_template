import time
import concurrent.futures
import queue
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random_number
import browser_automation
import random
import signal
import sys
from datetime import datetime

# Initialize a thread-safe queue to store start and end times along with instance identifiers and success status
result_queue = queue.Queue()

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

class TestTest2():
    def __init__(self, driver, MeetingURL, instance_id):
        self.driver = driver
        self.MeetingURL = MeetingURL
        self.start = None
        self.end = None
        self.instance_id = instance_id  # Store instance identifier
        self.success = False  # Initialize success status
    
    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    
    def refresh_tabs(self, refresh_percent):
        window_handles = self.driver.window_handles
        num_tabs = len(window_handles)
        tabs_to_refresh = int(num_tabs * (refresh_percent / 100))
        
        for idx, handle in enumerate(window_handles):
            self.driver.switch_to.window(handle)
            self.driver.refresh()
            if idx + 1 >= tabs_to_refresh:
                break
    
    def test_test2(self):
        try:
            self.start = time.time()
            print(f"Instance {self.instance_id} started at {format_timestamp(self.start)}")
            
            self.driver.get(self.MeetingURL)
            time.sleep(10)
            self.driver.set_window_size(1620, 1010)
            time.sleep(5)
            self.driver.find_element(By.ID, "btnToSignin").click()
            time.sleep(5)
            self.driver.find_element(By.ID, "select2-ddlUnit-container").click()
            time.sleep(random.randint(10,15))
            self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(random_number.select_random_number())
            time.sleep(random.randint(10,15))
            self.driver.find_element(By.CSS_SELECTOR, ".select2-search__field").send_keys(Keys.ENTER)
            time.sleep(random.randint(10,15))
            self.driver.find_element(By.ID, "btnPE1").click()
            time.sleep(random.randint(10,15))
            self.driver.find_element(By.ID, "txtVerCode").click()
            time.sleep(25)
            self.driver.find_element(By.ID, "txtVerCode").send_keys("112233")
            time.sleep(25)            
            self.driver.find_element(By.ID, "btnP1").click()
            time.sleep(25)
            self.driver.find_element(By.CSS_SELECTOR, ".btn_SinedInNormal").click()
            time.sleep(25)
            
            # Mark success if reached this point
            self.success = True
            self.end = time.time()
            print(f"Instance {self.instance_id} ended at {format_timestamp(self.end)}")
            result_queue.put((self.instance_id, self.start, self.end, self.success))

            self.refresh_tabs(refresh_percent=0)
            time.sleep(1800)
                
        except Exception as e:
            self.end = time.time()
            print(f"Exception occurred in instance {self.instance_id}: {str(e)}")
            result_queue.put((self.instance_id, self.start, self.end, self.success))  # Ensure result is recorded even on failure
        finally:
            self.teardown_method()
            self.driver.quit()

def run_test(instance_num):
    driver = webdriver.Chrome()
    test_instance = TestTest2(driver, MeetingURL, instance_num + 1)  # Pass instance number (1-based index)
    try:
        test_instance.test_test2()
    finally:
        driver.quit()
        print(f"Instance {instance_num + 1} finished.")

def signal_handler(sig, frame):
    print("\nInterrupt received. Exiting...")
    results = []
    while not result_queue.empty():
        instance_id, start, end, success = result_queue.get()
        results.append((instance_id, format_timestamp(start), format_timestamp(end), success))
    print(results)
    print("All start and end times:")
    for instance_id, start, end, success in results:
        print(f"({instance_id} - {start}, {end} - {success})")
    sys.exit(0)

def main(num_instances, interval=4):
    signal.signal(signal.SIGINT, signal_handler)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_instances) as executor:
        futures = []
        for instance_num in range(num_instances):
            # Submit test to executor
            future = executor.submit(run_test, instance_num)
            futures.append(future)
            # Wait for the interval before submitting the next instance
            time.sleep(interval)
        
        try:
            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received. Exiting...")
    
    # Collect and print all start and end times if not interrupted
    results = []
    while not result_queue.empty():
        instance_id, start, end, success = result_queue.get()
        results.append((instance_id, format_timestamp(start), format_timestamp(end), success))
    
    print(results)
    print("All start and end times: \n")
    for instance_id, start, end, success in results:
        print("Computer A")
        print(f"{instance_id} - {start}, {end} - {success})")

if __name__ == "__main__":
    num_instances = 30  # Number of instances to run concurrently
    MeetingURL = "https://blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2873"
    main(num_instances)