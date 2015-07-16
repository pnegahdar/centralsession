CentralSession
==============

[![Build Status](https://travis-ci.org/pnegahdar/centralsession.svg?branch=master)](https://travis-ci.org/pnegahdar/centralsession) [![Coverage Status](https://coveralls.io/repos/pnegahdar/centralsession/badge.svg?branch=master&service=github)](https://coveralls.io/github/pnegahdar/centralsession?branch=master)

Service architecture needs a centralized session store for various frameworks and languages.

The app is designed to be pluggable with new frameworks etc and is backed by redis.

Note since this only currently supports a cache backend hmac signing as needed with traditional cookie based storage is unnecessary

### Usage ###

#### Django ####

Install

    pip install centralsession

Settings.py
    
    INSTALLED_APPS += ('centralsession',)
     
    CENTRAL_SESSION_KEY_PREFIX = 'centralsession'
    CENTRAL_SESSION_REDIS_URI = 'redis://localhost:6379'
    SESSION_ENGINE = 'centralsession.django_session'


#### Flask ####

Install

    pip install centralsession


Config:

    from centralsession import flask_session
    redis_uri =  'redis://localhost:6379/0'
    app.session_interface = flask_session.CentralSessionInterface(redis_uri)


