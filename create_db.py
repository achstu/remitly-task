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
        row = list(map(lambda f: f.strip() if f else None, row))
        Bank.create(**dict(zip(columns, row)))

db.close()
