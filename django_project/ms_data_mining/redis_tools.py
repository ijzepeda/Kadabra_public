import hashlib
import json
from datetime import timedelta
from django.db import models
import redis
from ms_data_mining.settings import REDIS_DB, REDIS_HOST, REDIS_PORT


class TimeTypeEnum(models.TextChoices):
    DAYS = "days"
    SECONDS = "seconds"
    MICROSECONDS = "microseconds"
    MILLISECONDS = "milliseconds"
    MINUTES = "minutes"
    HOURS = "hours"
    WEEKS = "weeks"


class Utils:
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def flush_all(self):
        self.r.flushdb()

    @staticmethod
    def get_time_delta(frequency: TimeTypeEnum, time_data):
        frequency = TimeTypeEnum(frequency).value

        kwargs = {frequency: time_data}

        return timedelta(**kwargs)

    @staticmethod
    def get_unique_name(group_name, term):
        bytes_filters = bytes(term, "utf-8")
        hash_filters = hashlib.sha1(bytes_filters).hexdigest()
        return f"{group_name}-{hash_filters}"

    def get_data(self, key):
        try:
            data = self.r.get(key)
            if data is not None:
                data = json.loads(data)
        except Exception as ex:
            data = None
            print(ex)

        return data

    def set_data(self, key, value, time_type: TimeTypeEnum, time_data):
        try:
            data = json.dumps(value)
            self.r.setex(key, Utils.get_time_delta(time_type, time_data), value=data)
        except Exception as ex:
            print(ex)

    def delete_data(self, key):
        self.r.delete(key)

    def delete_data_by_patter(self, key_pattern):
        pattern = key_pattern
        item_count = 0
        batch_size = 100000
        keys = []

        for k in self.r.scan_iter(pattern, count=batch_size):
            keys.append(k)
            if len(keys) >= batch_size:
                item_count += len(keys)

                self.r.delete(*keys)
                keys = []

        if len(keys) > 0:
            item_count += len(keys)

            self.r.delete(*keys)
