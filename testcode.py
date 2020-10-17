import json
import requests
import base64

def gethtml(url):
    try:

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36'
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

#获取赛题列表
def getchallengelist():
    url = "http://47.102.118.1:8089//api/challenge/list"
    # 每次请求的结果都不一样，动态变化
    datalist = json.loads(gethtml(url))
    for t in datalist:
        print(t)

#获取队伍记录
def getrecord(id):
    url = "http://47.102.118.1:8089/api/teamdetail/"+str(id)
    # 每次请求的结果都不一样，动态变化
    text = json.loads(gethtml(url))
    rank = text["rank"]
    score = text["score"]
    success = text["success"]
    fail = text["fail"]
    unsolved = text["unsolved"]
    print("rank = ",rank)
    print("score = ",score)
    print("fail = ", fail)
    print("unsolved = ", unsolved)
    for i in range(43):
        print("uuid = ",success[i]["challengeid"])
        print("本题排名 = ",success[i]["rank"])

def getproblem():
    url = "http://47.102.118.1:8089/api/problem?stuid=031802435"
    # 每次请求的结果都不一样，动态变化
    text = json.loads(gethtml(url))
    img_base64 = text["img"]
    step = text["step"]
    swap = text["swap"]
    uuid = text["uuid"]
    img = base64.b64decode(img_base64)
    # 获取接口的图片并写入本地
    with open("photo.jpg", "wb") as fp:
        fp.write(img)  # 900*900
    return step,swap,uuid

#获取具体赛题
def getchallenge(uuid):
    url = "http://47.102.118.1:8089/api/challenge/start/" + uuid
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({
    "teamid": 21,
    "token": "a8aee99c-f29b-42c6-abd0-72216d8d851c"
    })
    r = requests.post(url, headers=headers, data=data_json)
    text = json.loads(r.text)
    chanceleftleft = text["chanceleft"]
    data = text["data"]
    img_base64 = data["img"]
    step = data["step"]
    swap = data["swap"]
    success = text["success"]
    img = base64.b64decode(img_base64)
    uuid = text["uuid"]
    expire = text["expire"]
    with open("photo.jpg", "wb") as fp:
        fp.write(img)  # 900*900
    return step, swap, uuid
#提交答案
def postAnswer(uuid,operations,swap):
        url ="http://47.102.118.1:8089/api/challenge/submit"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36',
            'Content-Type': 'application/json'
        }
        data_json = json.dumps({
            "uuid": uuid,
            "teamid": 24,
            "token": "a8aee99c-f29b-42c6-abd0-72216d8d851c",
            "answer": {
                "operations": operations,
                "swap": swap}}
        )
        r=requests.post(url,headers = headers,data = data_json)
        print(r.text)
#获取未做赛题
def getunsloved():
    url = "http://47.102.118.1:8089/api/team/problem/21"
    text = json.loads(gethtml(url))
    print(text)
#获取总排名
def getrank():
    url = "http://47.102.118.1:8089/api/rank"
    text = json.loads(gethtml(url))
    for i in text:
        print(i)

