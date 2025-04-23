# script for scrapping spreadsheet (csv) to sqlite3 database
import csv
from model import Bank


db = Bank._meta.database
db.connect()
db.create_tables([Bank])

with open("swift_codes.csv", newline="") as file:
    reader = csv.reader(file)
    columns = list(map(lambda col: col.replace(" ", "_").lower(), next(reader)))

    for row in reader:
        row = [field.strip() if field.strip() else None for field in row]
        args = dict(zip(columns, row))
        args['is_headquarter'] = args['swift_code'].endswith('XXX')
        Bank.create(**args)

db.close()
