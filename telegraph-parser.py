import requests
import random
import os
import sys
шаблон = '<HTML><HEAD><META HTTP-EQUIV="REFRESH" CONTENT="0; URL=---"></HEAD><BODY></BODY></HTML>'
month = 1
day = 1
lnk = input("Your request > ")
valid = 0
alls = 0
uselogging = input("[Using] Logging? [y|n] > ").lower()
mode = input(
    "[Choose] Mode -> HtmlLinks/HtmlLinks+txt/txt [h|ht|t] > ").lower()
if mode not in ["h", "ht", "t"]:
    print("[Error] Unknown arg [MODE]")
    print("[PressKey] Press any key to exit")
    input()
    sys.exit()
print("[Parser] Starting Parser...")
if mode in ["h", "ht"] and not os.path.isdir("parsed"):
    os.mkdir("parsed")
while True:
    alls += 1
    l = f"{lnk}-{str(month).zfill(2)}-{str(day).zfill(2)}"
    url = f"https://telegra.ph/{l}"
    if uselogging == "y":
        print("[Parser] Requesting \"" + l + "\"")
    try:
        rq = requests.get(url)
    except:
        print(f"[Parser] CAN'T CONNECT TO \"{l}\"! SKIPPING...")
        continue
    if rq.status_code == 200:
        if mode in ["h", "ht"]:
            open("parsed/" + l + ".html",
                 "w").write(шаблон.replace("URL=---", url))
        if mode in ["t", "ht"]:
            open("parsed.txt", "a").write(url + "\n")
        if uselogging == "y":
            print("[Parser] Link is valid")
        valid += 1
    else:
        if uselogging == "y":
            print("[Parser] Link is invalid (python syntax be like)")
    day += 1
    if day == 32:
        day = 1
        month += 1
    if month >= 12:
        print("=================\n[Parser] Parsing Ended")
        print(f"[Parser] Checked[{alls}]|Valid[{valid}]")
        print("[PressKey] Press any key to exit")
        input()
        break
