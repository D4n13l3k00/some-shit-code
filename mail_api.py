#############################################################
#         Simple mobile API wrapper for Mail.Cloud          #
#                     Coded by D4n13l3k00                   #
#       github.com/Daniel3k00         t.me/d4n13l3k00       #
# For download file,  you must use useragent from this code #
#############################################################
from requests import post
import re
class MailAPI():
    def __init__(self, user_agent:str="Android 3.15.6.11343.10:BASIC:ru.mail.cloud::null"):
        self.videos = ['.MPG', '.MOV', '.WMV', '.AVI', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.asf', '.asx', '.avi', '.bin', '.dat', '.drv', '.f4v', '.flv', '.gtp', '.h264', '.m4v', '.mkv', '.mod', '.moov', '.mov', '.mp4', '.mpeg', '.mpg', '.mts', '.rm', '.rmvb', '.spl', '.srt', '.stl', '.swf', '.ts', '.vcd', '.vid', '.vid', '.vid', '.vob', '.webm', '.wm', '.wmv', '.yuv', '.mp4']
        self.photos = ['.asf', '.cdw', '.cr2', '.cs', '.cur', '.dmp', '.drv', '.icns', '.ico', '.max', '.mds', '.mng', '.msv', '.odt', '.pct', '.pict', '.png', '.pps', '.prf', '.spl', '.tex', '.ttf', '.xps', '.jpg', '.jpeg', '.bmp', '.webp', '.raw']
        self.audios = ['.WAV', '.AIF', '.MP3', '.MID', '.aac', '.ac3', '.aif', '.aiff', '.amr', '.aob', '.ape', '.asf', '.aud', '.aud', '.aud', '.aud', '.awb', '.bin', '.bwg', '.cdr', '.flac', '.gpx', '.ics', '.iff', '.m', '.m3u', '.m3u8', '.m4a', '.m4b', '.m4p', '.m4r', '.mid', '.midi', '.mod', '.mp3', '.mp3', '.mp3', '.mpa', '.mpp', '.msc', '.msv', '.mts', '.nkc', '.ogg', '.ps', '.ra', '.ram', '.sdf', '.sib', '.sln', '.spl', '.srt', '.srt', '.temp', '.vb', '.wav', '.wav', '.wave', '.wm', '.wma', '.wpd', '.xsb', '.xwb', '.oga']
        self.headers = {"user-agent":user_agent}
        self.url = re.compile(r"(http(s)*://)*(cloud.mail.ru/)*/*(.*)")
    def get_list(self, path:str, limit:int=1000, offset:int=0) -> dict:
        if not self.url.match(path):
            raise ValueError(f"Url/path \"{path}\" is invalid!")
        path = self.url.findall(path)[0][-1]
        l = {"info":None,"videos":[], "photos":[], "audios":[], "other":[], "dirs":[]}
        obj = post("https://mublic.cloud.mail.ru/api/m3/list", headers=self.headers, json={"path":path, "limit":limit, "offset":offset, "direction":"asc", "sort":"name"}).json()
        for i in obj["objects"]:
            if i["type"] == "f":
                if "."+i["name"].split(".")[-1] in self.videos:
                    l["videos"].append([i["name"], post("https://mublic.cloud.mail.ru/api/m3/get", headers=self.headers,json={"path":path+"/"+i["name"]}).json()["url"]])
                elif "."+i["name"].split(".")[-1] in self.photos:
                    l["photos"].append([i["name"], post("https://mublic.cloud.mail.ru/api/m3/get", headers=self.headers,json={"path":path+"/"+i["name"]}).json()["url"]])
                elif "."+i["name"].split(".")[-1] in self.audios:
                    l["audios"].append([i["name"], post("https://mublic.cloud.mail.ru/api/m3/get", headers=self.headers,json={"path":path+"/"+i["name"]}).json()["url"]])
                else:
                    l["other"].append([i["name"], post("https://mublic.cloud.mail.ru/api/m3/get", headers=self.headers,json={"path":path+"/"+i["name"]}).json()["url"]])
            elif i["type"] == "d":
                l["dirs"].append(i["name"])
            else:
                pass
        l["info"] = {"name":obj["name"], "files":obj["files"]}
        return l
    def get_list_raw(self, path:str, limit:int=1000, offset:int=0) -> dict:
        if not self.url.match(path):
            raise ValueError(f"Url/path \"{path}\" is invalid!")
        path = self.url.findall(path)[0][-1]
        return post("https://mublic.cloud.mail.ru/api/m3/list", headers=self.headers,json={"path":path, "limit":limit, "offset":offset, "direction":"asc", "sort":"name"}).json()
    def get_url(self, path:str) -> str:
        if not self.url.match(path):
            raise ValueError(f"Url/path \"{path}\" is invalid!")
        path = self.url.findall(path)[0][-1]
        return post("https://mublic.cloud.mail.ru/api/m3/get", headers=self.headers, json={"path":path}).json()["url"]