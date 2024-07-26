import requests
from time import sleep

def validate_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.RequestException:
        return False

def get_meeting_url():
    while True:
        meeting_url = input("Please Enter the Meeting URL: ")
        if validate_url(meeting_url):
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
