import sys

from scraper.ridi_monthly_calendar import print_new_book_count_by_day

if __name__ == "__main__":
    event_id = sys.argv[1] if len(sys.argv) >= 2 else None
    if event_id is None:
        print(f"Usage : {sys.argv[0]} [event_id]")
        print(f"Example : {sys.argv[0]} 18622")
        exit(1)

    print_new_book_count_by_day(event_id)
