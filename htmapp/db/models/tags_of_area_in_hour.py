# -*- coding: utf-8 -*-
from htmapp.db.models.simple_area import SimpleArea
from peewee import *
from htmapp.db.db_engine import get_db

db = MySQLDatabase(None, threadlocals=True)

class TagsOfAreaInHour(Model):
    area = ForeignKeyField(SimpleArea, related_name='tags_in_hour')
    max_stamp = DateTimeField()
    min_stamp = DateTimeField()
    processed = DateTimeField(null=True)

    class Meta:
        database = get_db()
        indexes = (
            (('area', 'max_stamp'), True),
            (('area', 'min_stamp'), True)
        )