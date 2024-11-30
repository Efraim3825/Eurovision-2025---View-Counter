### ESC_2025_Viewcounter

import sys
print(sys.executable)

### Importing modules
from googleapiclient.discovery import build
import csv
from datetime import datetime
import time

def is_youtube_link(string):
    return 'www.youtube.com/watch' in string

def youtube_url_to_video_id(url):
    video_id = url.replace('https://www.youtube.com/watch?v=','')
    return video_id

### Create a function to get current view counts
my_API_KEY = '' # type the name of your YouTube Data API v3 project key into the quotation marks

def get_video_views(url, api_key = my_API_KEY):
    """
    Takes the url of a YouTube- video and tells you how many views it currently has. If the video doesn't exist, that counts as 0 views

    Parameters:
    @ url (string): full url of the video
    @ api_key (string): the API- key to your YouTube Data API v3 project

    Returns:
    @ views (int): the view count of the video, or 0 if the video doesn't exist
    """
    if not is_youtube_link(url):
        return 0
    video_id = youtube_url_to_video_id(url)
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part='statistics', id=video_id)
    response = request.execute()
    views = int(response['items'][0]['statistics']['viewCount'])
    return views

def create_views_list(file_path):
    """
    Reads through the second row of a csv file, starting with the second column. Said second row should contain strings, especially YouTube URLs, or be empty. 
    Creates a list containing the current view count of every video in any given cell, or 0 if that cell doesn't contain a YouTube URL.

    Parameters:
    @ file_path (string): Path to your csv file. Remember to put '.csv' at the end.

    Returns:
    @ views_list (list[int]): the view counts of all the videos in the second row. Any cells with no video URL are being count as having 0 views.
    """
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    # Read the second row. if you want to read the n'th row instead, change the 1 to n-1
    second_row = rows[1]
    
    views_list = [get_video_views(video_id) for video_id in second_row][1:]
    
    return views_list

### Function for automatically writing data in a CSV- file
# Save the data in a CSV-file
def log_views_to_csv(views_list, file_path):
    """
    Takes a csv file, and appends the given views_list below the last row of the file. The file is being updated in-place. 

    Parameters:
    @ views_list (list[int]): list of views as created by the create_views_list- function
    @ file_path (string): Path to your csv file. Remember to put '.csv' at the end.

    Returns:
    None
    """
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now()] + views_list)


### Main program
## Automatically collect the views for every URL in your log.

log_name = "ESC_2025_Viewcounter_log.csv" # the name of the csv- file where you want to log the view counts.

views_list = create_views_list(log_name)
log_views_to_csv(views_list, log_name)
