from __future__ import unicode_literals
import random
import string
import json
import functools

import redis

DneError = LookupError("The session does not yet exists. Create one using create_key")


def serialize(data):
    """
    Serialize the data
    :param data: a json serializable flat k/v dict
    :return: the json string dump
    """
    return json.dumps(data)


def deserialize(data):
    """
    Deserialize the data
    :param data: a json serializable flat k/v dict
    :return: the json string dump
    """
    return json.loads(data)


class SessionBackend():
    def __init__(self, redis_uri):
        self.redis_con = redis.from_url(redis_uri)


    def _get_random_key(self, len=32):
        allowed_chars = string.ascii_letters + string.digits
        randomizer = random.SystemRandom()
        return ''.join((randomizer.choice(allowed_chars) for _ in xrange(len)))


    def create_session(self, key, expires):
        """
        Creates a session with the expiry, empty dict for now
        :param expires: seconds to expire
        :return: the randomly generated key
        """
        expires = int(expires)
        if not key:
            key = self._get_random_key()
        self.redis_con.set(key, json.dumps({}), expires)
        return key


    @staticmethod
    def _set_key_txn(session_key, data_key, data_value, pipe):
        """
        A method used to do the atomic dict modification
        :param session_key: the key for the session will create if DNE
        :param data_key:
        :param data_value:
        :param pipe:
        :return:
        """
        data_raw = pipe.get(session_key)
        data = json.loads(data_raw)
        data[data_key] = data_value
        pipe.set(session_key, serialize(data))


    def exists(self, session_key):
        return self.redis_con.exists(session_key)

    def set_key(self, session_key, data_key, data_value):
        """
        Set the session key
        :param session_key: the key for the session will create if DNE
        :param data_key: the key of the data point being added to the session
        :param data_value: the value of the data being added to the session
        :return: `dict` containing the final key/value pairs
        """
        data_raw = self.redis_con.get(session_key)
        if not data_raw:
            raise DneError
        data = deserialize(data_raw)
        data[data_key] = data_value
        txn_partial = functools.partial(SessionBackend._set_key_txn, session_key, data_key,
                                        data_value)
        return self.redis_con.transaction(txn_partial, session_key)[0]


    def save(self, session_key, data, expire):
        """
        Set the session key
        :param session_key: the key for the session will create if DNE
        :param data: the data to be saved
        :param expire: when to expire the data
        """
        self.redis_con.set(session_key, serialize(data), expire)
        return


    def get_session(self, session_key):
        """
        Get the session Data
        :param session_key:
        :return: the deserialized data
        """
        data_raw = self.redis_con.get(session_key)
        if not data_raw:
            raise DneError
        return deserialize(data_raw)


    def delete_session(self, session_key):
        self.redis_con.delete(session_key)
        return True
