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


### Spec ###

Always use standard json serializer/deserializer nothing custom.

##### Create Session ######

args:

    expires - Seconds till expiry
    data - A flat (preferably) K : V json string
    secret - Some secret key ie os.urandom(24)

proc:

     session_key = 32 Char random string
     data_hashed = hash(data)
     redis SET session_key `data` expires

return: `session_key`

##### Set Data ######

args:

    session_key
    data - A flat (preferably) K : V json string

proc:

     redis SET session_key data


##### Set Key ######

args:

    session_key
    key = the key to store the data in
    value = the value of the key

proc:

     redis WATCH session_key
     data_raw = redis GET session_key
     data = json.loads(data_raw)
     data[k] = v
     redis MULTI
     redis SET session_key json.dumps(data)
     redis EXEC

##### Get full Session ######

args:

    session_key

proc:

     redis GET session_key


##### Destroy Session ######


args:

    session_key

proc:

     redis DELETE session_key


*Note the python implementation in python/session.py is probably most useful here*



