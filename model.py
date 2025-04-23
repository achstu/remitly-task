from peewee import Model, TextField, FixedCharField, SqliteDatabase

class Bank(Model):
    country_iso2_code = TextField()
    swift_code = FixedCharField(primary_key=True, max_length=16)
    code_type = TextField()
    name = TextField()
    address = TextField(null=True)
    town_name = TextField()
    country_name = TextField()
    time_zone = TextField()

    class Meta:
        database = SqliteDatabase('banks.db')
        table_name = 'banks'
