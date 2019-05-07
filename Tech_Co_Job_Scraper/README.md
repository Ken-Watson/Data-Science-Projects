This is a website scraper I built to scrape job search results from Amazon, Apple, Facebook, Google, and Netflix. It takes a little over 4 hours to scrape all the jobs from all the websites but it works without crashing, at least at the time of this entry.

For Amazon, you will need to have your own Crawlera account or some other proxy network and place that on line 73. Amazon will block you if you do not have this because this script takes a little over 4 hours to run and they will notice.

To run the whole thing, you will need to have all files in one folder and run the 'scraper_main.py' file. It will create separate CSV file for each company but also one large CSV file with all jobs included.
