import requests
import re
import json
import random
__url = "https://duckduckgo.com/"


def picsfw(q):
    params = {
        'q': str(q)
    }
    res = requests.post(__url, data=params)
    i = requests.get(f"https://duckduckgo.com/i.js?o=json&q={q}&"+re.search(
        r'vqd=([\d-]+)&', res.text, re.M | re.I)[0])
    i = json.loads(i.text)
    ii = i['results']
    random.shuffle(ii)
    try:
        return ii[0]
    except:
        return None


def picnsfw(q):
    params = {
        'q': str(q)
    }
    res = requests.post(__url, data=params)
    i = requests.get(f"https://duckduckgo.com/i.js?o=json&p=-1&q={q}&"+re.search(
        r'vqd=([\d-]+)&', res.text, re.M | re.I)[0])
    i = json.loads(i.text)
    ii = i['results']
    random.shuffle(ii)
    try:
        return ii[0]
    except:
        return None


def getjsonsfw(q):
    params = {
        'q': str(q)
    }
    res = requests.post(__url, data=params)
    i = requests.get(f"https://duckduckgo.com/i.js?o=json&q={q}&"+re.search(
        r'vqd=([\d-]+)&', res.text, re.M | re.I)[0])
    i = json.loads(i.text)
    return i


def getjsonnsfw(q):
    params = {
        'q': str(q)
    }
    res = requests.post(__url, data=params)
    i = requests.get(f"https://duckduckgo.com/i.js?o=json&p=-1&q={q}&"+re.search(
        r'vqd=([\d-]+)&', res.text, re.M | re.I)[0])
    i = json.loads(i.text)
    return i
