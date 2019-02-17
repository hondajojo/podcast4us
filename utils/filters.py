# coding:utf-8

import re, datetime, pytz
from localtime import tz, timenow

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

_RE_WEIBO = re.compile(ur'\d{1,2}')


def weibodate(s):
    l = _RE_WEIBO.findall(s)
    lenght = len(l)
    now = timenow()
    if lenght == 1:
        date = now - datetime.timedelta(minutes=int(l[0]))
    elif lenght == 2:
        date = datetime.datetime(now.year, now.month, now.day, *map(int, l), tzinfo=tz)
    elif lenght == 4:
        date = datetime.datetime(now.year, *map(int, l), tzinfo=tz)
    elif lenght == 5:
        date = datetime.datetime(*map(int, l), tzinfo=tz)
    else:
        date = now
    return date.strftime("%a, %d %b %Y %H:%M:%S %z")


def zhihudate(date, hour):
    return datetime.datetime.strptime(date + hour[-2:], '%Y%m%d%H') \
        .replace(tzinfo=tz) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def weixindate(timestamp):
    return datetime.datetime.utcfromtimestamp(int(timestamp)) \
        .replace(tzinfo=pytz.utc).astimezone(tz) \
        .strftime("%a, %d %b %Y %H:%M:%S %z")


def rsplit(s, count):
    f = lambda x: x > 0 and x or 0
    return [s[f(i - count):i] for i in range(len(s), 0, -count)]


def id2mid(id):
    result = ''
    for i in rsplit(id, 7):
        str62 = base62_encode(int(i))
        result = str62.zfill(4) + result
    return result.lstrip('0')


def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
