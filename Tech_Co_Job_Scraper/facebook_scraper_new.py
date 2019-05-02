from time import time
from datetime import datetime
from time import sleep
from random import randint
from requests import get
from IPython.core.display import clear_output
from warnings import warn
import lxml
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import tempfile

# Facebook Job Search URL
'''
https://www.facebook.com/careers/jobs?page=1&results_per_page=100&locations[0]=Fremont%2C%20CA&
locations[1]=Northridge%2C%20CA&locations[2]=San%20Francisco%2C%20CA&locations[3]=Santa%20Clara%2C%20CA&
locations[4]=Mountain%20View%2C%20CA&locations[5]=Los%20Angeles%2C%20CA&locations[6]=Seattle%2C%20WA&
locations[7]=Woodland%20Hills%2C%20CA&locations[8]=Sunnyvale%2C%20CA&locations[9]=Menlo%20Park%2C%20CA&
locations[10]=Redmond%2C%20WA#search_result
'''


def get_all_jobs(pages):
    requests = 0
    start_time = time()
    total_runtime = datetime.now()
    for page in pages:
        response = get("https://www.facebook.com/careers/jobs/?page={}&results_per_page=100"
                       "&locations[0]=Fremont%2C%20CA&locations[1]=Northridge%2C%20CA&"
                       "locations[2]=San%20Francisco%2C%20CA&locations[3]=Santa%20Clara%2C%20CA&"
                       "locations[4]=Mountain%20View%2C%20CA&locations[5]=Los%20Angeles%2C%20CA&"
                       "locations[6]=Seattle%2C%20WA&locations[7]=Woodland%20Hills%2C%20CA&"
                       "locations[8]=Sunnyvale%2C%20CA&locations[9]=Menlo%20Park%2C%20CA&"
                       "locations[10]=Redmond%2C%20WA#search_result".format(page))

        # Monitor the frequency of requests
        requests += 1

        # Pauses the loop between 8 - 15 seconds and marks the elapsed time
        sleep(randint(8, 15))
        current_time = time()
        elapsed_time = current_time - start_time
        print("Facebook Request:{}; Frequency: {} request/s; Total Run Time: {}".format(requests,
              requests / elapsed_time, datetime.now() - total_runtime))
        clear_output(wait=True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn("Request: {}; Status code: {}".format(requests, response.status_code))

        # Set page requests. Break the loop if number of requests is greater than expected
        if requests > 19:
            warn("Number of requests was greater than expected.")
            break

        yield from get_job_infos(response)


def get_job_infos(response):
    page_soup = BeautifulSoup(response.text, "lxml")
    job_containers = page_soup.find_all("a", "_69jm")
    for container in job_containers:
        site = page_soup.find("title").text
        title = container.find("div", "_69jo").text
        location = container.find("div", "_1n-z _6hy- _21-h").text
        job_link = "https://www.facebook.com" + container.get("href")
        yield site, title, location, job_link


def main():
    # Set the number of pages to scrape
    pages = [str(i) for i in range(1, 19)]

    # Writes to a temp file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, newline='', encoding="utf-8") as temp_csv:
        writer = csv.writer(temp_csv)
        writer.writerow(["Website", "Title", "Location", "Job URL"])
        writer.writerows(get_all_jobs(pages))

        # Reads the temp file into a data frame for output to csv file
        fb_df = pd.read_csv(temp_csv.name)
        fb_df = fb_df.join(fb_df['Location'].str.split('\W+(?=\s[A-Z][a-z])', expand=True)
                           .add_prefix('city_').fillna(np.nan))
        fb_df = fb_df.set_index(list(fb_df.columns.values[0:4])).stack()
        fb_df = fb_df.reset_index()
        fb_df['Location'] = fb_df.iloc[:, -1].str.strip()
        fb_df.drop(fb_df.columns[[-1, -2]], axis=1, inplace=True)
        fb_df.to_csv('facebook_jobs.csv', index=False)


if __name__ == "__main__":
    main()
