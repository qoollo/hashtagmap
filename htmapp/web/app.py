# -*- coding: utf-8 -*-
from flask import Flask, render_template, make_response

# configure
app = Flask(__name__)
app.config.from_object('htmapp.default_settings')
app.config.from_envvar('HASHTAGMAP_SETTINGS', silent=True)

# init db
from htmapp.db.models import *
db.init(app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'])


@app.route('/')
def hello_world():
    location = Location.get()

    lat_km = (location.north - location.south) / location.height * 1000
    long_km = (location.east - location.west) / (location.north_width + location.south_width) * \
        2 * 1000

    areas = location.simple_areas
    max_count = location.simple_areas.order_by(SimpleArea.most_popular_tag_count.desc()).first().most_popular_tag_count
    return render_template('index.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km, location=location)


@app.route('/<tag_name>')
def counts(tag_name):
    location = Location.get()

    lat_km = (location.north - location.south) / location.height * 1000
    long_km = (location.east - location.west) / (location.north_width + location.south_width) * \
        2 * 1000

    areas = location.simple_areas
    max_count = 0
    print 'Done1'
    for a in areas:
        count = a.count_of_tag(tag_name)
        a.c = count
        if count > max_count:
            max_count = count
    print 'Done2'
    return render_template('counts.html', areas=areas, max_count=max_count, lat_km=lat_km, \
        long_km=long_km, location=location)