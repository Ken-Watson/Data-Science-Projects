import amazon_scraper_new
import apple_scraper_new
import google_scraper_new
import netflix_scraper_new
import facebook_scraper_new
import glob


if __name__ == "__main__":
    amazon_scraper_new.main()
    apple_scraper_new.main()
    google_scraper_new.main()
    netflix_scraper_new.main()
    facebook_scraper_new.main()

all_job_files = glob.glob("*.csv")

header_saved = False
with open('job_list_new.csv', 'w') as f_out:
    for filename in all_job_files:
        with open(filename) as f_in:
            header = next(f_in)
            if not header_saved:
                f_out.write(header)
                header_saved = True
            for line in f_in:
                f_out.write(line)
