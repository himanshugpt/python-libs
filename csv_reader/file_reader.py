import csv
import logging
import argparse

class CSVReader:

    CSV_HEADERS = []

    def __init__(self, filename):
        self.logger = self.set_up_logging()
        self.filename = filename
        self.records = []

    def set_up_logging(self):
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(format=FORMAT)
        logger = logging.getLogger('CSVReader')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def process_data(self):
        with open(self.filename,'rt') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                obj = {}
                for name in CSV_HEADERS:
                    obj[name] = row[name]
                self.records.append(obj)

    def transform(self, transformFunc, args):
        try:
            transformFunc(*args)
        except:
            self.logger.error("transformation function failed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processed csv File')
    parser.add_argument('file', help='path of csv file')
    args = parser.parse_args()
    filename = args.file
    reader = CSVReader(filename=filename)
    reader.set_up_logging()
    reader.process_data()
