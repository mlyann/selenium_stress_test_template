import time
import os
import numpy as np
import matplotlib.pyplot as plt
import wget_valid_input

# https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2704
MeetingURL = wget_valid_input.get_meeting_url()
DURATION_MINUTES = wget_valid_input.get_float_input("Please Enter the Duration Time (minutes): ")  # Duration in minutes for the script to run
TIME_LINE = wget_valid_input.get_int_input("Please Tell Me Maximum Acceptable Response Time (seconds): ")
PAUSE_TIME_EXCEED  = wget_valid_input.get_int_input("Number of Seconds to Pause Each Request if it exceeds the time line (seconds): ")
PAUSE_TIME_NOT_EXCEED = wget_valid_input.get_int_input("Number of Seconds to Pause Each Request if it doesn't exceed the time line (seconds): ")

import time
import os

def collect_load_times(MeetingURL, duration_minutes, recordfile):
    end_time = time.time() + duration_minutes * 60
    start_time = time.time()
    timestamps = []
    load_times = []
    i = 0
    try:
        with open(recordfile, 'w') as f:
            f.write("Meeting URL \t "+MeetingURL+" \n" )
            f.write(f"Duration (minutes) \t{DURATION_MINUTES}\n")
            f.write(f"Maximum acceptable response time (seconds) \t{TIME_LINE}\n")
            f.write(f"Pause time if exceeds the time line (seconds) \t{PAUSE_TIME_EXCEED}\n")
            f.write(f"Pause time if does not exceed the time line (seconds) \t{PAUSE_TIME_NOT_EXCEED}")
            f.write("Timestamp \t Loading Times (seconds) \tPause Each Request (seconds) \tIS ACCEPTABLE? \n")

        while time.time() < end_time:

            ACCEPT = True

            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = end_time - current_time
            
            start = time.time()
            filename = f"MeetingStatusReport_{i}.aspx"
            os.system(f'wget {MeetingURL} -O {filename}')
            end = time.time()
            os.system(f"rm {filename}")
            delta = end - start

            print("--------------------Loading Time--------------------")
            print(f"Delta: {delta:.2f} seconds")
            print(f"Elapsed Time: {elapsed_time:.2f} seconds")
            print(f"Remaining Time: {remaining_time:.2f} seconds")
            print("----------------------------------------------------")
            
            if delta < TIME_LINE:
                pause = PAUSE_TIME_NOT_EXCEED  # Pause between requests
            else:
                pause = PAUSE_TIME_EXCEED
                ACCEPT = False
                
            time.sleep(pause)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start))
            line = f"{timestamp} \t {delta:.2f} \t {pause} \t {ACCEPT} \n"

            with open(recordfile, 'a') as f:
                f.write(line)

            timestamps.append(timestamp)
            load_times.append(delta)
            
            i += 1

    except KeyboardInterrupt:
        print("Interrupted! Saving current data...")

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
        f"Counts of Exceeding Loading Time Line ({stats['mean']} seconds): {stats['count_exceeding']}\n"
        f"Mean of Loading Time: {stats['mean']}\n"
        f"Median of Loading Time: {stats['median']}\n"
        f"Max of Loading Time: {stats['max']}\n"
        f"Min of Loading Time: {stats['min']}\n"
    )

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, load_times, marker='o', linestyle='-')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Timestamp')
    plt.ylabel('Loading Time (s)')
    plt.title('Webpage Loading Times Over Multiple Requests')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print(stats)

def generate_filename(url, minutes):
    # Extract a simple identifier from the URL (e.g., the meeting ID)
    base_name = url.split('?')[-1]  # Assumes query string has relevant info
    return f"LoadTimes_{base_name}_{minutes}min.txt"

def print_loading_times(timestamps, load_times, filename):
    print("Timestamp and Loading Times:")
    print("----------------------------")
    for timestamp, load_time in zip(timestamps, load_times):
        line = f"{timestamp}: {load_time:.2f} seconds\n"
        print(line, end='')
    print("----------------------------")
    print(f"Data saved to {filename}")


def main():
    filename = generate_filename(MeetingURL, DURATION_MINUTES)
    timestamps, load_times = collect_load_times(MeetingURL, DURATION_MINUTES,filename)
    if timestamps and load_times:
        stats = calculate_statistics(load_times, TIME_LINE)
        plot_load_times(timestamps, load_times, stats)
        print_loading_times(timestamps, load_times, filename)
        print(MeetingURL)
    else:
        print("No data collected.")
        print(MeetingURL)

if __name__ == "__main__":
    main()
