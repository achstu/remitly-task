from fastapi import FastAPI, HTTPException, status
from model import Bank, db
from pydantic import BaseModel

app = FastAPI()


class BankCreateRequest(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str


@app.get(
    "/v1/swift_codes/{swift_code}",
    description="Retrieve details of a single SWIFT code whether for a headquarters or branches.",
)
def bank_by_code(swift_code: str):
    bank = Bank.get_or_none(Bank.swift_code == swift_code.upper())
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    response = {
        "address": bank.address,
        "bankName": bank.bank_name,
        "countryISO2": bank.country_iso2,
        "countryName": bank.country_name,
        "isHeadquarter": bank.is_headquarter,
        "swiftCode": bank.swift_code,
    }

    if bank.is_headquarter:
        branches = bank.get_branches()
        response["branches"] = [
            {
                "address": branch.address,
                "bankName": branch.bank_name,
                "countryISO2": branch.country_iso2,
                "isHeadquarter": branch.is_headquarter,
                "swiftCode": branch.swift_code,
            }
            for branch in branches
        ]

    return response


@app.get(
    "/v1/swift_codes/country/{countryISO2code}",
    description="Return all SWIFT codes with details for a specific country (both headquarters and branches).",
)
def bank_by_county(countryISO2code: str):
    countryISO2code = countryISO2code.upper()

    banks = Bank.select().where(Bank.country_iso2_code == countryISO2code)
    if not banks:
        raise HTTPException(status_code=404, detail="No banks found for this country")

    country_name = banks[0].country_name

    return {
        "countryISO2": countryISO2code,
        "countryName": country_name,
        "swiftCodes": [
            {
                "address": bank.address,
                "bankName": bank.bank_name,
                "countryISO2": bank.country_iso2,
                "isHeadquarter": bank.is_headquarter,
                "swiftCode": bank.swift_code,
            }
            for bank in banks
        ],
    }


@app.post(
    "/v1/swift_codes",
    description="Adds new SWIFT code entries to the database for a specific country.",
    status_code=status.HTTP_201_CREATED,
)
def add_bank(bank_data: BankCreateRequest):
    if Bank.get_or_none(Bank.swift_code == bank_data.swiftCode.upper()):
        raise HTTPException(status_code=400, detail="SWIFT code already exists")

    try:
        bank = Bank.create(
            swift_code=bank_data.swiftCode.upper(),
            bank_name=bank_data.bankName,
            address=bank_data.address,
            country_iso2=bank_data.countryISO2.upper(),
            country_name=bank_data.countryName.upper(),
            is_headquarter=bank_data.isHeadquarter,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating bank: {str(e)}")

    return {"message": "Bank created successfully"}


@app.delete(
    "/v1/swift_codes/{swift_code}",
    description="Deletes swift-code data if swiftCode matches the one in the database.",
)
def delete_bank(swift_code: str):
    bank = Bank.get_or_none(Bank.swift_code == swift_code.upper())
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    if len(bank.get_branches()) > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete headquarters that has branches",
        )

    bank.delete_instance()
    return {"message": "Bank deleted successfully"}
