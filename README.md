CentralSession
==============

Service architecture needs a centralized session store for various frameworks and languages.

The app is designed to be pluggable with new frameworks etc and is backed by redis.

Note since this only currently supports a cache backend hmac signing as needed with traditional cookie based storage is unnecessary

### Usage ###

#### Django ####

Install

    pip install centralsession


Settings.py

    CENTRAL_SESSION_REDIS_URI = 'redis://localhost:6479/0'
    SESSION_ENGINE = 'central_session.providers.django_session'


#### Flask ####

Install

    pip install centralsession


Config:

    from centralsession.python.providers import flask_session
    redis_uri =  'redis://localhost:6479/0'
    app.session_interface = flask_session.CentralSessionInterface(redis_uri)


