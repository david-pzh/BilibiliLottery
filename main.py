from utils import *

if __name__ == "__main__":
    Dynamic_id = str(GetDynamicid())
    print("获取动态成功，ID为：" + Dynamic_id)
    print("正在获取转发数据中......\n")
    users = GetUsers(Dynamic_id)
    total = GetTotalRepost(Dynamic_id)
    for index, user in enumerate(users):
        print("[{}] {}({}) Hash({})".format(index, user["uid"], user["name"], user["hash"]))
    print("获取成功!获取到的转发人数(去重后):%i人, 实际转发人数:%i人, 相差%i人" % (len(users)-1, total, total-len(users)))
    lucky_num = input("\n---请粘贴随机数种子：---\n")
    lucky_num = hashlib.sha256(lucky_num.encode("utf-8")).hexdigest()

    print("\n【开奖号码为：{}】".format(lucky_num))
    n = input("\n---请输入奖品数量(1~{})：---\n".format(len(users)))

    lucky_num = int(lucky_num, 16)
    users = sorted(users, key=lambda i: abs(int(i['hash'], 16) - lucky_num))

    print("\n【获奖用户为：】")
    for i in range(int(n)):
        print(users[i])
        print("\n")