from time import time
from time import sleep
from datetime import datetime
from requests import get
from random import randint
from random import choice
from IPython.core.display import clear_output
from warnings import warn
import json
import csv

''' Amazon Job Search URL:
https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=relevant&job_type=Full-Time&
cities[]=Seattle%2C%20Washington%2C%20USA&cities[]=San%20Francisco%2C%20California%2C%20USA&
cities[]=Sunnyvale%2C%20California%2C%20USA&cities[]=Bellevue%2C%20Washington%2C%20USA&
cities[]=East%20Palo%20Alto%2C%20California%2C%20USA&cities[]=Santa%20Monica%2C%20California%2C%20USA&
category_type=Corporate&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=USA&base_query=&
city=&country=USA&region=&county=&query_options=& 
'''


def get_all_jobs(pages):
    requests = 0
    start_time = time()
    total_runtime = datetime.now()
    user_agent_list = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

        # Firefox
        'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0'
        'Mozilla/5.0 (X11; U; Linux Core i7-4980HQ; de; rv:32.0; compatible; JobboerseBot; http://www.jobboerse.com/bot.htm) Gecko/20100101 Firefox/38.0'
        'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0'
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    ]

    for page in pages:
        try:
            user_agent = choice(user_agent_list)
            headers = {'User-Agent': user_agent}

            response = get('https://www.amazon.jobs/en/search.json?base_query=&city=&country=USA&county=&'
                           'facets%5B%5D=location&facets%5B%5D=business_category&facets%5B%5D=category&'
                           'facets%5B%5D=schedule_type_id&facets%5B%5D=employee_class&facets%5B%5D=normalized_location'
                           '&facets%5B%5D=job_function_id&job_function_id%5B%5D=job_function_corporate_80rdb4&'
                           'latitude=&loc_group_id=&loc_query=USA&longitude=&'
                           'normalized_location%5B%5D=Seattle%2C+Washington%2C+USA&'
                           'normalized_location%5B%5D=San+Francisco'
                           '%2C+California%2C+USA&normalized_location%5B%5D=Sunnyvale%2C+California%2C+USA&'
                           'normalized_location%5B%5D=Bellevue%2C+Washington%2C+USA&'
                           'normalized_location%5B%5D=East+Palo+Alto%2C+California%2C+USA&'
                           'normalized_location%5B%5D=Santa+Monica%2C+California%2C+USA&offset={}&query_options=&'
                           'radius=24km&region=&result_limit=10&schedule_type_id%5B%5D=Full-Time&'
                           'sort=relevant'.format(page),
                           headers=headers,
                           # You will need your own Crawlera account and place below.
                           proxies={
                               "http": "http://xxxxxxxxxxxxxxxxxxxxxxx:@proxy.crawlera.com:8010/"
                           }
                           )

            # Monitor the frequency of requests
            requests += 1

            # Pauses the loop between 8 - 15 seconds and marks the elapsed time
            sleep(randint(8, 15))
            current_time = time()
            elapsed_time = current_time - start_time
            print("Amazon Request:{}; Frequency: {} request/s; Total Run Time: {}".format(requests,
                  requests / elapsed_time, datetime.now() - total_runtime))
            clear_output(wait=True)

            # Throw a warning for non-200 status codes
            if response.status_code != 200:
                warn("Request: {}; Status code: {}".format(requests, response.status_code))

            # Set page requests. Break the loop if number of requests is greater than expected
            if requests > 999:
                warn("Number of requests was greater than expected.")
                break
            yield from get_job_infos(response)

        except AttributeError as e:
            print(e)
            continue


def get_job_infos(response):
    amazon_jobs = json.loads(response.text)
    for website in amazon_jobs['jobs']:
        site = website['company_name']
        title = website['title']
        location = website['normalized_location']
        job_link = 'https://www.amazon.jobs' + website['job_path']
        yield site, title, location, job_link


def main():
    # Page range starts from 0 and the middle value increases by 10 each page.
    pages = [str(i) for i in range(0, 9990, 10)]

    # Writes to csv file
    with open('amazon_jobs.csv', "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Website", "Title", "Location", "Job URL"])
        writer.writerows(get_all_jobs(pages))


if __name__ == "__main__":
    main()
