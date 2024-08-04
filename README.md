# Selenium Load Testing Project

This project demonstrates the use of Selenium WebDriver for automated browser testing and concurrent execution using threading in Python. The script performs load testing by opening multiple browser instances and interacting with a web application. 

## Table of Contents

- [Selenium Load Testing Project](#selenium-load-testing-project)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the Load Test](#running-the-load-test)
  - [Selecting a Random Number](#selecting-a-random-number)
  - [Running the Wget URL Test](#running-the-wget-url-test)
  - [Browser Automation](#browser-automation)
  - [Project Structure](#project-structure)
  - [Contribution (Thank you!)](#contribution-thank-you)

## Installation

1. Clone the repository:

```bash
git clone https://gitlab.coretechs.com/blackstone/blackstone-load-testing-script.git
cd blackstone-load-testing-script
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```
3. Download the ChromeDriver and place it in a directory included in your system's PATH.


## Usage

### Running the Load Test

To run the load test with multiple instances:

```bash
python main.py
```

The num_instances variable in main_script.py determines the number of concurrent browser instances to run. You can adjust it as needed.



## Selecting a Random Number

The script `random_number.py` contains a function to select a random number from a predefined list. You can use this function as needed in your tests.

## Running the Wget URL Test

The script `wget_test.py` demonstrates how to use `wget` to download files and measure the download time. To run it:

```bash
python wget_test.py
```

## Browser Automation

The `BrowserAutomation` class in `browser_automation.py` provides functionality to open multiple tabs in the browser and navigate to a specified URL. You can initialize this class and use its methods in your tests.



## Project Structure

```
selenium-load-testing/
├── main_script.py            # Main script to run the load test
├── random_number.py          # Script to select a random number
├── wget_test.py              # Script to perform wget URL test
├── browser_automation.py     # Browser automation class
├── test_script.py            # Test class with Selenium tests
├── requirements.txt          # Project dependencies
└── README.md                 # Project README file
```
* `main_script.py`: Contains the main function to run multiple instances of Selenium tests concurrently.
* `random_number.py`: Provides a function to select a random number from a predefined list.
* `wget_test.py`: Demonstrates downloading files using `wget` and measuring the time taken.
* `browser_automation.py`: Defines the `BrowserAutomation` class for browser operations.
* `test_script.py`: Contains the `TestTest2` class which performs the Selenium tests.
* `requirements.txt`: Lists the Python packages required for the project.
* `README.md`: This README file.



## Contribution
Minglai Yang
