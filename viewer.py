import argparse
import os
from config import load_config, Config
from datetime import datetime, timedelta

SCRIPT_PATH = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CFG_PATH = os.path.join(SCRIPT_PATH, "config.cfg")

class Entry:
    def __init__(self, timestamp: datetime, msg: str) -> None:
        self.timestamp = timestamp
        self.msg = msg

    def print(self):
        print(self.timestamp, self.msg)


class Log:
    def __init__(self, filename, all):
        self.filename = filename
        with open(filename, 'r') as data:
            self.data = data.read()
        self.accessed: list[Entry] = []
        self.find_accessed(all)

    def find_accessed(self, all):
        data_list = self.data.split("\n")
        for line in data_list:
            if line and (all or "INFO" in line):
                timestamp_str = line.split("[")[1].split("]")[0]
                try:
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    self.accessed.append(Entry(timestamp, line.split("]")[1]))
                except ValueError as e:
                    print(f"Error parsing timestamp: {e}")
                    continue

    def from_day(self, day):
        target_day = datetime.strptime(day, "%Y-%m-%d")
        for entry in self.accessed:
            if entry.timestamp.date() == target_day.date():
                entry.print()

    def from_range(self, start, end):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        for entry in self.accessed:
            if start_date.date() <= entry.timestamp.date() <= end_date.date():
                entry.print()

    def print(self):
        for entry in self.accessed:
            entry.print()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Parse and display log file entries.")
    parser.add_argument("--config","-c", help='Path to print server config file.', default=DEFAULT_CFG_PATH)
    parser.add_argument("--day", help="Show entries for a specific day (YYYY-MM-DD).")
    parser.add_argument("--from", dest="start", help="Start of date range (YYYY-MM-DD).")
    parser.add_argument("--to", dest="end", help="End of date range (YYYY-MM-DD).")
    parser.add_argument("--today", action="store_true", help="Show entries for today.")
    parser.add_argument("--yesterday", action="store_true", help="Show entries for yesterday.")
    parser.add_argument("--all", action="store_true", help="Show failed print attempts")
    return parser.parse_args()


def main():
    args = parse_arguments()

    path_to_cfg = args.config
    config: Config = load_config(path_to_cfg)
    log = Log(config.logging.log_path, args.all)
    # Handle the new arguments
    if args.today:
        today = datetime.now().strftime("%Y-%m-%d")
        log.from_day(today)
    elif args.yesterday:
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        log.from_day(yesterday)
    elif args.day:
        log.from_day(args.day)
    elif args.start and args.end:
        log.from_range(args.start, args.end)
    else:
        log.print()


if __name__ == "__main__":
    main()
