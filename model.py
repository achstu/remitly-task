from peewee import Model, TextField, FixedCharField, BooleanField, SqliteDatabase

db = SqliteDatabase("banks.db")


class Bank(Model):
    swift_code = FixedCharField(primary_key=True, max_length=11)
    bank_name = TextField()
    address = TextField()
    country_iso2 = FixedCharField(max_length=2)
    country_name = TextField()
    is_headquarter = BooleanField()

    class Meta:
        database = db
        table_name = "banks"

    def get_branches(self):
        if not self.is_headquarter:
            return []

        return Bank.select().where(
            (Bank.swift_code.startswith(self.swift_code[:8]))
            & (Bank.is_headquarter == False)
        )
