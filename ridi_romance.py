import config
import scraper

if __name__ == "__main__":
    ridi_session = scraper.login(config.ACCOUNT_ID, config.ACCOUNT_PASSWORD)
    if not ridi_session:
        exit(1)
    scraper.get_today_recommendation(ridi_session)
