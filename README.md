# Selenium Load Testing Project

This project demonstrates the use of Selenium WebDriver for automated browser testing and concurrent execution using threading in Python. The script performs load testing by opening multiple browser instances and interacting with a web application. 

## Table of Contents

- [Selenium Load Testing Project](#selenium-load-testing-project)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Running the Load Test](#running-the-load-test)
  - [Selecting a Random Number](#selecting-a-random-number)
  - [Browser Automation](#browser-automation)
    - [Output Format and Data Description:](#output-format-and-data-description)
    - [Data Structure:](#data-structure)
  - [Additional Information](#additional-information)
  - [Project Structure](#project-structure)
  - [Contribution (Thank you!)](#contribution-thank-you)

## Installation

1. Clone the repository:

```bash
git clone https://gitlab.coretechs.com/blackstone/blackstone-load-testing-script.git
cd blackstone-load-testing-script
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```
4. Download the ChromeDriver and place it in a directory included in your system's PATH. If you downloaded Chrome, then you can skip this step.




### Running the Load Test

To run the load test with multiple instances:

```bash
python main.py
```


The ```num_instances``` variable in main.py determines the number of concurrent browser instances to run. You can adjust it as needed.

The ```interval``` variable determines how long of a pause there is between when each user is launched.

```Both variables can be found at the bottom of main.py```

## Selecting a Random Number

The script `random_number.py` contains a function to select a random number from a predefined list. You can use this function as needed in your tests.

There are two lists of homeowners, use whichever is loaded into the roster.


## Browser Automation

The `BrowserAutomation` class in `browser_automation.py` provides functionality to open multiple tabs in the browser and navigate to a specified URL. You can initialize this class and use its methods in your tests.

### Output Format and Data Description:

The active_user_ranges.txt file stores data about user activity in a structured format. Each entry in the file represents a unique user session on a website, detailing when the session began, when it ended, and whether the user successfully reached the final page of their session.

### Data Structure:

Each line in the file represents a single user session and contains the following elements, separated by commas: [User ID, Start Time, End Time, Success Indicator]:

* User ID: A unique identifier for the user.
* Start Time: The timestamp marking the beginning of the user session.
* End Time: The timestamp marking the end of the user session.
* Success Indicator: A boolean value (True or False) indicating whether the user successfully reached the final page during the session.
```
eg. [(11, '2024-08-02 17:42:32', '2024-08-02 17:43:32', False), (24, '2024-08-02 17:43:24', '2024-08-02 17:44:28', False), (1, '2024-08-02 17:41:51', '2024-08-02 17:44:38', True), (2, '2024-08-02 17:41:54', '2024-08-02 17:44:51', True),....]
```


## Additional Information

- For larger load tests, the blackstone website may load slower than the steps can be reached which will cause the tab/user to automatically close. To combat this, time.sleep() has been added in between each step. If you experience less than 70% of users making it to the landing page, consider increasing the time.sleep(). 
- On start and end time the script will print to terminal when each instance starts/ends, if the script is keyboard interrupted then it will return a list of tuples with each instance ID, start time, end time, and a boolean representing whether it got to the landing page.


## Project Structure

```
selenium-load-testing/
├── random_number.py          # Script to select a random number
├── browser_automation.py     # Browser automation class
├── main.py                  # Selenium launcher and Main
├── requirements.txt          # Project dependencies
└── README.md                 # Project README file
```

* `random_number.py`: Provides a function to select a random number from a predefined list.
* `browser_automation.py`: Defines the `BrowserAutomation` class for browser operations.
* `main.py`: Contains the `TestTest2` class which performs the Selenium tests.
* `requirements.txt`: Lists the Python packages required for the project.
* `README.md`: This README file.



## Contribution (Thank you!)
Ming and Gavin under James, Jawad, and Susan's instruction.
Special thanks to James, Jawad, and Susan.