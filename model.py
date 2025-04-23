import peewee

class Bank(peewee.Model):
    country_iso2_code = peewee.TextField()
    swift_code = peewee.FixedCharField(primary_key=True, max_length=16)
    code_type = peewee.TextField()
    name = peewee.TextField()
    address = peewee.TextField(null=True)
    town_name = peewee.TextField()
    country_name = peewee.TextField()
    time_zone = peewee.TextField()

    class Meta:
        database = peewee.SqliteDatabase('banks.db')
        table_name = 'banks'
