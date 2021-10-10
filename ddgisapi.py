#############################################################
#                DuckDuckGo ImagesSearch API                #
#                    Coded by D4n13l3k00                    #
#        github.com/D4n13l3k00       t.me/D4n13l3k00        #
#############################################################
#           Required : aiohttp[speedups] pydantic           #
#############################################################
import re
from typing import *

import aiohttp
from pydantic import BaseModel


class Image(BaseModel):
    title: str
    source: str
    thumbnail: str
    image: str
    url: str
    width: int
    height: int


class Images(BaseModel):
    images: List[Image]


class DuckDuckGoImagesSearchAPI:

    def __init__(self):
        self._url = "https://duckduckgo.com/"
        self._biurl = 'i.js'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
        self._sfw_params = {
            'o': 'json'
        }
        self._nsfw_params = self._sfw_params
        self._nsfw_params['p'] = '-1'

    @staticmethod
    def __parse_kv(string: str) -> Tuple[str, str]:
        data = re.search(r'vqd=([\d-]+)&', string, re.M | re.I)[0]
        data = (data[:len(data)-1]).split('=')
        return data

    async def getPictures(self, search: str, nsfw: bool = False) -> Images:
        async with aiohttp.ClientSession(headers=self._headers) as s:
            params = self._nsfw_params if nsfw else self._sfw_params
            params['q'] = search
            async with s.post(self._url, data={'q': search}) as rsp:
                __ = self.__parse_kv(await rsp.text())
                params[__[0]] = __[1]
            async with s.get(self._url+self._biurl, params=params) as rsp:
                return Images(images=(await rsp.json(content_type=None))['results'])
