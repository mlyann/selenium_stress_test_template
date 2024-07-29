"""
Webpage Loading Time Tester

Author: Minglai Yang

This script measures and analyzes the loading times of a specific webpage at regular intervals for a given duration. It utilizes `wget` to fetch the page, records the loading times, and provides statistics and visualizations to evaluate performance.

Modules:
- `wget_valid_input`: A module to handle user input with validation for meeting URL, duration, and response times.

Functions:
- `collect_load_times(MeetingURL, duration_minutes, recordfile)`: Collects loading times for a given meeting URL over a specified duration. Records data to a file.
  - Parameters:
    - `MeetingURL` (str): The URL of the meeting page to test.
    - `duration_minutes` (float): The duration in minutes for which to run the test.
    - `recordfile` (str): The filename to which the collected data will be saved.
  - Returns:
    - `timestamps` (list of str): Timestamps of each request.
    - `load_times` (list of float): Corresponding loading times.

- `calculate_statistics(load_times, loading_time_line)`: Computes statistics from the recorded loading times.
  - Parameters:
    - `load_times` (list of float): List of loading times.
    - `loading_time_line` (float): The maximum acceptable loading time.
  - Returns:
    - `stats` (dict): A dictionary containing count of exceeding times, mean, median, max, and min loading times.

- `plot_load_times(timestamps, load_times, stats)`: Plots the loading times against timestamps and prints statistics.
  - Parameters:
    - `timestamps` (list of str): Timestamps of each request.
    - `load_times` (list of float): Corresponding loading times.
    - `stats` (dict): Statistics about the loading times.

- `generate_filename(url, minutes)`: Generates a filename based on the URL and duration for saving the collected data.
  - Parameters:
    - `url` (str): The meeting URL.
    - `minutes` (float): The duration of the test in minutes.
  - Returns:
    - `filename` (str): The generated filename.

- `print_loading_times(timestamps, load_times, filename)`: Prints the collected loading times and saves them to a file.
  - Parameters:
    - `timestamps` (list of str): Timestamps of each request.
    - `load_times` (list of float): Corresponding loading times.
    - `filename` (str): The filename where the data was saved.

- `main()`: The main function that orchestrates the entire process. It collects loading times, calculates statistics, generates plots, and prints results.

Usage:
1. Modify the `wget_valid_input` module if needed to adjust how inputs are obtained and validated.
2. Run the script. It will prompt for a meeting URL, duration, and response times.
3. The script will output loading times, statistics, and visualizations to evaluate the performance of the webpage.

Notes:
- Ensure `wget` is installed and accessible in your environment.
- The `matplotlib` library is used for plotting graphs.
- If interrupted, the script will save the current data and exit gracefully.

"""


import time
import os
import numpy as np
import matplotlib.pyplot as plt
import requests
from tqdm import tqdm

import wget_valid_input
import pyfiglet

ascii_art = pyfiglet.figlet_format("Blackstone")
print(ascii_art)

time.sleep(3)

def print_introduction():
    print("================================================================================")
    print("                           Webpage Load Time Monitor                           ")
    print("================================================================================")
    print("Author: Coretechs Consulting Inc.")
    print("Date: July 26, 2024")
    print("Description:")
    print("This script measures the loading times of a webpage over a specified duration.")
    print("It records the loading times and checks if they exceed a given acceptable response time.")
    print("The results are saved to a file and visualized using a plot.")
    print("================================================================================\n")

# Print introduction at the start of the program
print_introduction()




# https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2704
MeetingURL = wget_valid_input.get_meeting_url()
print("Enter Meeting URL Successfully!!")
DURATION_MINUTES = wget_valid_input.get_float_input("Please Enter the Duration Time (minutes): ")  # Duration in minutes for the script to run
print("Enter Duration Time Successfully!!")
TIME_LINE = wget_valid_input.get_int_input("Please Tell Me Maximum Acceptable Response Time (seconds): ")
print("Enter Maximum Acceptable Response Time Successfully!!")
PAUSE_TIME_NOT_EXCEED = wget_valid_input.get_int_input("Number of Seconds to Pause Each Request If It Does NOT EXCEED Maximum Acceptable Response Time  (seconds): ")
print("Enter Acceptable Loading Page's Pausing Time Successfully!!")
PAUSE_TIME_EXCEED  = wget_valid_input.get_int_input("Number of Seconds to Pause Each Request If It EXCEED Maximum Acceptable Response Time (seconds): ")
print("Enter Unacceptable Loading Page's Pausing Time Successfully!!")


# Calculate the maximum length for the content lines
max_length = max(len("Meeting URL " + MeetingURL),
                 len(f"Duration (minutes) {DURATION_MINUTES}"),
                 len(f"Maximum acceptable response time (seconds) {TIME_LINE}"),
                 len(f"Pause time if exceeds the time line (seconds) {PAUSE_TIME_EXCEED}"),
                 len(f"Pause time if does not exceed the time line (seconds) {PAUSE_TIME_NOT_EXCEED}"))

# Define the total width of the box
box_width = max_length + 4
print("\n\n")
# Print the box
print("*" * box_width)
print("* " + "Meeting URL " + MeetingURL + " " * (box_width - 4 - len("Meeting URL " + MeetingURL)) + " *")
print(f"* Duration (minutes) {DURATION_MINUTES} " + " " * (box_width - 4 - len(f"Duration (minutes) {DURATION_MINUTES}")) + "*")
print(f"* Maximum acceptable response time (seconds) {TIME_LINE} " + " " * (box_width - 4 - len(f"Maximum acceptable response time (seconds) {TIME_LINE}")) + "*")
print(f"* Pause time if exceeds the time line (seconds) {PAUSE_TIME_EXCEED} " + " " * (box_width - 4 - len(f"Pause time if exceeds the time line (seconds) {PAUSE_TIME_EXCEED}")) + "*")
print(f"* Pause time if does not exceed the time line (seconds) {PAUSE_TIME_NOT_EXCEED} " + " " * (box_width - 4 - len(f"Pause time if does not exceed the time line (seconds) {PAUSE_TIME_NOT_EXCEED}")) + "*")
print("*" * box_width+"\n\n")


def collect_load_times(MeetingURL, duration_minutes, recordfile):
    end_time = time.time() + duration_minutes * 60
    start_time = time.time()
    timestamps = []
    load_times = []
    i = 0
    count = 0
    try:
        with open(recordfile, 'w') as f:
            f.write("Meeting URL \t "+MeetingURL+" \n" )
            f.write(f"Duration (minutes) \t{DURATION_MINUTES}\n")
            f.write(f"Maximum acceptable response time (seconds) \t{TIME_LINE}\n")
            f.write(f"Pause time if exceeds the time line (seconds) \t{PAUSE_TIME_EXCEED}\n")
            f.write(f"Pause time if does not exceed the time line (seconds) \t{PAUSE_TIME_NOT_EXCEED}\n")
            f.write("\n")
            f.write("\n")
            f.write("Data Records: \n")
            f.write("Timestamp \tTotal Elapsing Time (seconds) \tTotal Remaining Time (seconds) \tLoading Times (seconds) \tPause Each Request (seconds) \tIS ACCEPTABLE? \tTotal Counts of Exceeding Time Line\n")

        while time.time() < end_time:
            ACCEPT = True
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = end_time - current_time

            # Wget and Remove File
            start = time.time()
            filename = f"MeetingStatusReport_{i}.aspx"
            os.system(f'wget {MeetingURL} -O {filename}')
            end = time.time()
            os.system(f"rm {filename}")
            delta = end - start

            print("--------------------Current Data Report--------------------")
            print(f"Current Loading Time: {delta:.2f} seconds")
            print(f"Total Elapsed Time: {elapsed_time:.2f} seconds")
            print(f"Remaining Time: {remaining_time:.2f} seconds")
            print(f"Total Counts of Exceeding Time Line: {count}")
            print("-----------------------------------------------------------")

            if delta < TIME_LINE:
                pause = PAUSE_TIME_NOT_EXCEED  # Pause between requests
                print("")
                print(f"YES!! I am not exceeding your time line. Let's wait - {pause} - seconds.")
                print("")
            else:
                pause = PAUSE_TIME_EXCEED
                ACCEPT = False
                count += 1
                print("")
                print(f"Oops! I am exceeding your time line! Let's wait - {pause} - seconds. ")
                print("")

            time.sleep(pause)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
            line = f"{timestamp} \t{elapsed_time:.2f} \t{remaining_time:.2f} \t {delta:.2f} \t {pause} \t {ACCEPT}\t{count} \n"

            with open(recordfile, 'a') as f:
                f.write(line)

            timestamps.append(timestamp)
            load_times.append(delta)

            i += 1

    except KeyboardInterrupt:
        print("\n")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("! Interrupted! Saving current data...  !")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")

    return timestamps, load_times

def calculate_statistics(load_times, loading_time_line):
    stats = {}
    stats['count_exceeding'] = np.sum(np.array(load_times) > loading_time_line)
    stats['mean'] = np.mean(load_times)
    stats['median'] = np.median(load_times)
    stats['max'] = np.max(load_times)
    stats['min'] = np.min(load_times)

    return stats

def plot_load_times(timestamps, load_times, stats):
    print(
        f"Counts of Exceeding Loading Time Line ({TIME_LINE} seconds): {stats['count_exceeding']}\n"
        f"Mean of Loading Time: {stats['mean']}\n"
        f"Median of Loading Time: {stats['median']}\n"
        f"Max of Loading Time: {stats['max']}\n"
        f"Min of Loading Time: {stats['min']}\n"
        f"\n"
        f"Please Look at Our Plots!! \n"
        f"(And Close the Plot by red 'X') \n"
    )

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, load_times, marker='o', linestyle='-')
    plt.axhline(y=TIME_LINE, color='r', linestyle='--', label=f'Max Acceptable Time ({TIME_LINE}s)')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Timestamp')
    plt.ylabel('Loading Time (s)')
    plt.title('Webpage Loading Times Over Multiple Requests. ')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(stats)

def generate_filename(url, minutes):
    # Extract a simple identifier from the URL (e.g., the meeting ID)
    base_name = url.split('?')[-1]  # Assumes query string has relevant info
    return f"LoadTimes_{base_name}_{minutes}min.txt"

def print_loading_times(timestamps, load_times, filename):
    print("")
    print("Timestamp and Loading Times:")
    print("------------Head-------------")
    for timestamp, load_time in zip(timestamps, load_times):
        line = f"{timestamp}: {load_time:.2f} seconds\n"
        print(line, end='')
    print("-----------The End-----------")
    print("")
    print("-------------------------------------------------------")
    print(f"| Data saved to {filename} |")
    print("-------------------------------------------------------")

def main():
    filename = generate_filename(MeetingURL, DURATION_MINUTES)
    timestamps, load_times = collect_load_times(MeetingURL, DURATION_MINUTES, filename)
    if timestamps and load_times:
        stats = calculate_statistics(load_times, TIME_LINE)
        plot_load_times(timestamps, load_times, stats)
        print_loading_times(timestamps, load_times, filename)
        print("")
        print("")
        print("Meeting URL Again for Checking!")
        print(MeetingURL)
        print("")
        print("Thank you for using WGET testing product run by selenium.")
        print("Have a great day!")
        print("")

    else:
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!")
        print("! No data collected. !")
        print("!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        print("")
        print("Meeting URL Again for Checking!")
        print(MeetingURL)
        print("")
        print("Thank you for using WGET testing product run by Selenium.")
        print("Have a great day!")
        print("")

if __name__ == "__main__":
    main()
