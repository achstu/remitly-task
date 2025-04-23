from peewee import Model, TextField, FixedCharField, BooleanField, SqliteDatabase

db = SqliteDatabase("banks.db")


class Bank(Model):
    country_iso2_code = FixedCharField(max_length=2)
    swift_code = FixedCharField(primary_key=True, max_length=11)
    code_type = TextField(null=True)
    name = TextField()
    address = TextField(null=True)
    town_name = TextField(null=True)
    country_name = TextField()
    time_zone = TextField(null=True)
    is_headquarter = BooleanField()

    class Meta:
        database = db
        table_name = "banks"

    def get_branches(self):
        if not self.is_headquarter:
            return []

        return Bank.select().where(
            (Bank.swift_code.startswith(self.swift_code[:8])) & (Bank.is_headquarter == False)
        )
