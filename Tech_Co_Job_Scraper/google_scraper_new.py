from time import time
from time import sleep
from datetime import datetime
from requests import get
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import json
import re
import csv

# Google Job Search URL
'''
https://careers.google.com/jobs/results/?company=Google&company=YouTube&employment_type=FULL_TIME&hl=en_US&
jlo=en_US&location=California,%20USA&location=Oregon,%20USA&location=Washington,%20USA&page=1&q=&sort_by=relevance
'''


def get_all_jobs(pages):
    requests = 0
    start_time = time()
    total_runtime = datetime.now()
    for page in pages:
        # response = get("https://careers.google.com/api/jobs/jobs-v1/search/?company=Google&company=YouTube&"
        #                "employment_type=FULL_TIME&location={}%22%2C%20USA&page={}&q=&sort_by"
        #                "=relevance".format(city, page))
        response = get("https://careers.google.com/api/jobs/jobs-v1/search/?company=Google&company=YouTube&"
                       "employment_type=FULL_TIME&hl=en_US&jlo=en_US&location=California%2C%20USA&"
                       "location=Oregon%2C%20USA&location=Washington%2C%20USA&page={}&"
                       "q=&sort_by=relevance".format(page))

        # Monitor the frequency of requests
        requests += 1

        # Pauses the loop between 8 - 15 seconds and marks the elapsed time
        sleep(randint(10, 20))
        current_time = time()
        elapsed_time = current_time - start_time
        print("Google Request:{}; Frequency: {} request/s; Total Run Time: {}".format(requests,
              requests / elapsed_time, datetime.now() - total_runtime))
        clear_output(wait=True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn("Request: {}; Status code: {}".format(requests, response.status_code))

        # Set page requests. Break the loop if number of requests is greater than expected
        if requests > 86:  #88
            warn("Number of requests was greater than expected.")
            break

        yield from get_job_infos(response)


def get_job_infos(response):
    google_jobs = json.loads(response.text)
    for website in google_jobs['jobs']:
        google_job_id = website['job_id']
        try:
            found_id = re.search('jobs/(\d+)', google_job_id).group(1)
        except AttributeError:
            found_id = None
        site = website["company_name"]
        title = website["job_title"]
        location = website["location"]
        job_link = "https://careers.google.com/jobs/results/" + found_id
        yield site, title, location, job_link


def main():
    # Set the number of pages to scrape
    pages = [str(i) for i in range(1, 86)]

    # Writes to csv file
    with open('google_jobs.csv', "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Website", "Title", "Location", "Job URL"])
        writer.writerows(get_all_jobs(pages))


if __name__ == "__main__":
    main()
