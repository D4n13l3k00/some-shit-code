#############################################################
#       Simple async mobile API wrapper for MailCloud       #
#                    Coded by D4n13l3k00                    #
#        github.com/D4n13l3k00       t.me/D4n13l3k00        #
#############################################################
#           Required : aiohttp[speedups] pydantic           #
#############################################################
import re
from typing import *

import aiohttp
from pydantic import BaseModel


class Models:
    class NoFiles(BaseModel):
        pass

    class File(BaseModel):
        name: str
        url: str
        ttl: int = None
        mtime: int = None
        size: int = None

    class Directory(BaseModel):
        name: str

    class Files(BaseModel):
        name: str = None
        count: int = 0
        files: List = []


class MailAPI:

    def __init__(self, userAgent: str = "Android 3.16.0.12052 10:BASIC:ru.mail.cloud::null"):
        self.headers = {"user-agent": userAgent}
        self.url = re.compile(
            r"(https://){0,1}(cloud.mail.ru){0,1}(/){0,1}(public/.*)")

    async def isValidLink(self, link: str) -> bool:
        if not self.url.match(link):
            raise ValueError(f'Url/path \"{link}\" is invalid!')
        path = self.url.findall(link)[0][-1]
        async with aiohttp.ClientSession() as s, s.post("https://mublic.cloud.mail.ru/api/m3/list", headers=self.headers, json={
                "path": path, "limit": 1, "offset": 0, "direction": "asc", "sort": "name"}) as response:
            obj = await response.json()
            return 'objects' in obj or 'name' in obj

    async def getList(self, link: str, limit: int = 1000, offset: int = 0) -> Union[Models.Files, Models.File, Models.NoFiles]:
        if not self.url.match(link):
            raise ValueError(f'Url/path \"{link}\" is invalid!')
        path = self.url.findall(link)[0][-1]
        async with aiohttp.ClientSession() as s, s.post("https://mublic.cloud.mail.ru/api/m3/list", headers=self.headers, json={
                "path": path, "limit": limit, "offset": offset, "direction": "asc", "sort": "name"}) as response:
            obj = await response.json()

        if 'objects' not in obj:
            if 'name' in obj:
                async with aiohttp.ClientSession() as s, s.post("https://mublic.cloud.mail.ru/api/m3/get",
                                  headers=self.headers, json={"path": path}) as response:
                    j = (await response.json())
                    print(obj)
                    return Models.File(**obj, **j)
            return Models.NoFiles()
        result = Models.Files()
        for i in obj["objects"]:
            if i["type"] == "f":
                async with aiohttp.ClientSession() as s, s.post("https://mublic.cloud.mail.ru/api/m3/get",
                                  headers=self.headers, json={"path": path+"/"+i["name"]}) as response:
                    j = (await response.json())
                    result.files.append(Models.File(**i, **j))
            elif i["type"] == "d":
                result.dirs.append(Models.Directory(title=i["name"]))
        result.name = obj['name']
        result.count = obj['files']
        return result

    async def getFileLink(self, link: str) -> str:
        if not self.url.match(link):
            raise ValueError(f"Url/path \"{link}\" is invalid!")
        path = self.url.findall(link)[0][-1]
        async with aiohttp.ClientSession() as s, s.post("https://mublic.cloud.mail.ru/api/m3/get",
                          headers=self.headers, json={"path": path}) as response:
            j = await response.json()
            return j["url"] if "url" in j else None
