from model import Bank
from fastapi import FastAPI, HTTPException


app = FastAPI()
# db = Bank._meta.database


@app.get(
    "/v1/swift_codes/{swift_code}",
    description="Retrieve details of a single SWIFT code whether for a headquarters or branches.",
)
def bank_by_code(swift_code: str):
    bank = Bank.get_or_none(Bank.swift_code == swift_code)
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank.__data__


@app.get(
    "/v1/swift_codes/country/{countryISO2code}",
    description="Return all SWIFT codes with details for a specific country (both headquarters and branches).",
)
def bank_by_county(countryISO2code: str):
    banks = Bank.select().where(Bank.country_iso2_code == countryISO2code)
    for bank in banks:
        print(bank.name)
    return {}


@app.post(
    "/v1/swift_codes",
    description="Adds new SWIFT code entries to the database for a specific country.",
)
def add_bank():
    return {}


@app.delete(
    "/v1/swift_codes/{swift_code}",
    description="Deletes swift-code data if swiftCode matches the one in the database.",
)
def delete_bank(code: str):
    return {}
