import requests
import progressbar
import threading
import time
import queue

def show_progress(event):
    widgets = [
        'Progress: ', progressbar.Percentage(), ' ',
        progressbar.Bar(marker='=', left='[', right=']'), ' ',
        progressbar.ETA()
    ]
    duration = 10  # Duration for the progress bar
    bar = progressbar.ProgressBar(widgets=widgets, maxval=duration).start()
    
    for i in range(duration):
        if event.is_set():
            break
        time.sleep(0.1)  # Small sleep to update the progress bar
        bar.update(i + 1)
    
    bar.finish()

def validate_url(url, event, result_queue):
    try:
        response = requests.get(url)
        response.raise_for_status()
        result_queue.put(True)
    except requests.RequestException:
        result_queue.put(False)
    finally:
        event.set()

def validate_url_with_progress(url):
    event = threading.Event()
    result_queue = queue.Queue()
    
    progress_thread = threading.Thread(target=show_progress, args=(event,))
    validation_thread = threading.Thread(target=validate_url, args=(url, event, result_queue))

    progress_thread.start()
    validation_thread.start()

    validation_thread.join()
    progress_thread.join()

    return result_queue.get()

def get_meeting_url():
    while True:
        meeting_url = input("Please Enter the Meeting URL: ")
        if validate_url_with_progress(meeting_url):
            return meeting_url
        else:
            print("Invalid URL or the URL cannot be reached. Please try again.")


def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")
