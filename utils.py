import urllib.request
import json
import re
import hashlib

offset = ""
page = 0
users = []
# 定义一些全局变量

def GetDynamicid():
    s = input("---请粘贴Bilibili动态的网址：---\n（形如 https://t.bilibili.com/xxxxxxx）\n")
    nums = re.findall(r'\d+', s)
    return nums[0]

def GetTotalRepost(Dynamic_id):
    DynamicAPI = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=" + Dynamic_id
    BiliJson = json.loads(urllib.request.urlopen(DynamicAPI).read())
    Total_count = BiliJson['data']['card']['desc']['repost']

    return Total_count

def GetMiddleStr(content, startStr, endStr):
    startIndex = content.index(startStr)
    if startIndex >= 0:
        startIndex += len(startStr)
    endIndex = content.index(endStr)
    return content[startIndex:endIndex]

def getOffset(json):
    """
    获取分页的offset变量,会在每次的返回值中给出
    :json: 本页的json数据
    """
    if json['data']['has_more'] == 1:
        return json['data']['offset']
    else:
        return False

def GetUsers(Dynamic_id):
    global offset
    global users
    global page
    DynamicAPI = "https://api.live.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=" + Dynamic_id + "&offset=" + offset
    # 要想获取offset只能使用这个api
    BiliJson = json.loads(urllib.request.urlopen(DynamicAPI).read())
    # 全局Json
    UserJson = json.loads(str(GetMiddleStr(urllib.request.urlopen(DynamicAPI).read(), b"items\":", b",\"_gt_"), encoding = "utf-8"))
    # 获取到的分享用户json列表
    for dict in UserJson:
        # print(dict)
        Bilibili_UID = str(dict['desc']['user_profile']['info']['uid'])
        Bilibili_Uname = dict['desc']['user_profile']['info']['uname']
        # 这个api不支持获取评论,所以就砍掉了
        Bilibili_Hash = hashlib.sha256(Bilibili_UID.encode("utf-8")).hexdigest()
        user = {"uid": Bilibili_UID, "name": Bilibili_Uname, "hash": Bilibili_Hash}
        users.append(user)
    users = sorted(users, key=lambda i: int(i['hash'], 16))
    offset = getOffset(BiliJson)
    page += 1
    # 获取下一页的offset变量
    if offset:
        print("第%i页获取完成,Offset: %s" % (page, offset))
        return GetUsers(Dynamic_id)
        # 获取下一页
    else:
        tmpUsers = users
        users = []
        for user in tmpUsers:
            if user not in users:
                users.append(user)
        # 去重
        return users
        # 没有下一页了


def binarySearch(arr, l, r, x):
    if r >= l:
        mid = int(l + (r - l) / 2)
        if arr[mid] == x:
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid - 1, x)
        else:
            return binarySearch(arr, mid + 1, r, x)
    else:
        return l
