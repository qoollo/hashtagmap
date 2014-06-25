# -*- coding: utf-8 -*-
from .models import *
from .create_msk_location import *
from .create_areas_connections import *
from .. import config

db.init(config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD)

def drop_tables():
    if HashtagFrequency.table_exists():
    	HashtagFrequency.drop_table()
    	print '-- HashtagFrequency table dropped'

    if Hashtag.table_exists():
    	Hashtag.drop_table()
    	print '-- Hashtag table dropped'

    if SimpleArea.table_exists():
    	SimpleArea.drop_table()
    	print '-- SimpleArea table dropped'

    if Location.table_exists():
    	Location.drop_table()
	print '-- Location table dropped'


def create_tables():
    Location.create_table()
    print '++ Location table created'

    SimpleArea.create_table()
    print '++ SimpleArea table created'

    Hashtag.create_table()
    print '++ Hashtag table created'

    HashtagFrequency.create_table()
    print '++ HashtagFrequency table created'


def init_data():
    create_msk_location()
    create_areas_connections()
    

def clear_database():
    drop_tables()
    create_tables()
    init_data()