import datetime as dt
from functools import lru_cache
from app.config import Config

VERANLAGUNGSJAHR = 2021


def get_first_day_of_tax_period():
    return dt.date(VERANLAGUNGSJAHR, 1, 1)


def lru_cached(func):
    if Config.USE_LRU_CACHE:
        return lru_cache(func)

    return func
