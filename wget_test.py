import time
import os
import numpy as np

def wgetURL(MeetingURL, num, loading_time_line):
    """
    ------------------------------------------------------------------------------
    Here I add the loop for wget to observe the website responding time.
    ------------------------------------------------------------------------------
    """
    tc = np.array([])  # 初始化空的 NumPy 数组
    for i in range(num):
        start = time.time()
        filename = f"/Users/ming/Desktop/blackstone-load-testing-script/MeetingStatusReport_{i}.aspx"
        os.system(f'wget {MeetingURL} -O {filename}')
        end = time.time()
        os.system(f"rm {filename}")
        delta = end - start
        tc = np.append(tc, delta)  # 更新 tc 数组
    
    count = np.sum(tc > loading_time_line)
    mean_loading_time = np.mean(tc)
    median_loading_time = np.median(tc)
    max_loading_time = np.max(tc)
    min_loading_time = np.min(tc)
    
    print(
        f"Counts of Exceeding Loading Time Line ({loading_time_line} seconds): {count}\n"
        f"Mean of Loading Time: {mean_loading_time}\n"
        f"Median of Loading Time: {median_loading_time}\n"
        f"Max of Loading Time: {max_loading_time}\n"
        f"Max of Loading Time: {min_loading_time}\n"
    )

if __name__ == "__main__":
    MeetingURL = "https://blackstoneamoffice.com/editors/Reports/MeetingStatusReport.aspx?meetingid=2855"
    num = 100
    loading_time_line = 10
    wgetURL(MeetingURL, num, loading_time_line)

