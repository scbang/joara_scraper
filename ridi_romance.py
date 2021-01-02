import sys

import scraper

if __name__ == "__main__":
    account_id = sys.argv[1]
    account_password = sys.argv[2]
    scraper.scrape_romance_home(account_id, account_password)
    # scraper.test(account_id, account_password)
