import time
import os

def main(MeetingURL):
    """
    ------------------------------------------------------------------------------
    Here I add the loop for wget
    ------------------------------------------------------------------------------
    """
    for i in range(1):
        start = time.time()
        filename = f"/Users/ming/Desktop/blackstone-load-testing-script/MeetingStatusReport_{i}.aspx"
        os.system(f'wget {MeetingURL} -O {filename}')
        end = time.time()
        os.system(f"rm {filename}")
        delta = end-start
        if delta > 10:
            break
        else:
            print(f"Download {i}: {end-start} seconds")

if __name__ == "__main__":
    MeetingURL = "https://develop.blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2696"
    main(MeetingURL)
