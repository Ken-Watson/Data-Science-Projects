from time import time
from datetime import datetime
from requests import get
from time import sleep
from random import randint
from IPython.core.display import clear_output
from warnings import warn
import json
import csv

# Apple Job Search URL
'''
https://jobs.apple.com/en-us/search?location=seattle-SEA+los-angeles-metro-area-LAMETRO+
san-francisco-bay-area-SFMETRO+south-san-francisco-SSF+san-diego-SDO
'''


def get_all_jobs(pages):
    requests = 0
    start_time = time()
    total_runtime = datetime.now()
    for page in pages:
            response = get('https://jobs.apple.com/api/v1/search/page?location=seattle-SEA'
                           '%20los-angeles-metro-area-LAMETRO%20san-francisco-bay-area-SFMETRO'
                           '%20south-san-francisco-SSF%20san-diego-SDO&page={}'.format(page))

            # Monitor the frequency of requests
            requests += 1

            # Pauses the loop between 8 - 15 seconds and marks the elapsed time
            sleep(randint(8, 15))
            current_time = time()
            elapsed_time = current_time - start_time
            print("Apple Request:{}; Frequency: {} request/s; Total Run Time: {}".format(requests,
                  requests / elapsed_time, datetime.now() - total_runtime))
            clear_output(wait=True)

            # Throw a warning for non-200 status codes
            if response.status_code != 200:
                warn("Request: {}; Status code: {}".format(requests, response.status_code))

            # Set page requests. Break the loop if number of requests is greater than expected
            if requests > 108:
                warn("Number of requests was greater than expected.")
                break

            yield from get_job_infos(response)


def get_job_infos(response):
    apple_jobs = json.loads(response.text)
    for website in apple_jobs['searchResults']:
        site = 'Apple'
        title = website['postingTitle']
        location = website['locations'][0]['name']
        job_link = 'https://jobs.apple.com/en-us/details/' + website['positionId']
        yield site, title, location, job_link


def main():
    # Set the number of pages to scrape
    pages = [str(i) for i in range(1, 108)]

    # Writes to csv file
    with open('apple_jobs.csv', "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Website", "Title", "Location", "Job URL"])
        writer.writerows(get_all_jobs(pages))


if __name__ == "__main__":
    main()
