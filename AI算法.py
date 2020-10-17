import requests
import base64
import json
import math
import operator
import copy
import heapq
import random
import datetime
from functools import reduce
from PIL import Image
START = []  # 给定状态
END = []  # 目标状态
pathlist = ''  # 操作序列
# 4个方向
direction = [[0, 1], [0, -1], [1, 0], [-1, 0]]

# OPEN表
OPEN = []

# 节点的总数
SUM_NODE_NUM = 0


# 获取逆序对个数
def getStatus(list1):
    count = 0
    for i in range(len(list1)):
        if list1[i] != 0:
            for j in range(i):
                if list1[j] > list1[i]:
                    count += 1
    return count


# 判断是否有解
def judge(nowlist1, endlist1):
    nowlist = nowlist1[0] + nowlist1[1] + nowlist1[2]
    endlist = endlist1[0] + endlist1[1] + endlist1[2]
    num1 = getStatus(nowlist)
    num2 = getStatus(endlist)
    if num1 % 2 == num2 % 2:
        return True
    else:
        return False


# 在强制调换前随机移动
def getswaplist(nowlist, step):
    global pathlist
    while step:
        step -= 1
        for i in range(3):
            k = 0
            for j in range(3):
                dir = random.randint(0, 3)
                if nowlist[i][j] != 0:
                    continue
                x = i + direction[dir][0]
                y = j + direction[dir][1]
                while x < 0 or x >= 3 or y < 0 or y >= 3:
                    dir = random.randint(0, 3)
                    x = i + direction[dir][0]
                    y = j + direction[dir][1]
                nowlist[i][j], nowlist[x][y] = nowlist[x][y], nowlist[i][j]
                if dir == 0:
                    pathlist += 'd'
                elif dir == 1:
                    pathlist += 'a'
                elif dir == 2:
                    pathlist += 's'
                elif dir == 3:
                    pathlist += 'w'
                k = 1
                break
            if k == 1:
                break
    return nowlist


def get_fn(start, end):
    dist = 0
    N = len(start)
    for i in range(N):
        for j in range(N):
            if start[i][j] == end[i][j]:
                continue
            num = start[i][j]
            if num == 0:
                x = N - 1
                y = N - 1
            else:
                x = num / N  # 理论横坐标
                y = num - N * x - 1  # 理论的纵坐标
            dist += (abs(x - i) + abs(y - j))
    return dist


# 交换
def swaplist(nowlist, swap):
    a = swap[0]
    b = swap[1]
    i = int((a-1)/3)
    j = int((a-1)%3)
    x = int((b-1)/3)
    y = int((b-1)%3)
    nowlist[x][y], nowlist[i][j] = nowlist[i][j],nowlist[x][y]
    return nowlist


# 自由调换
def change(nowlist, endlist):
    min = 100000
    global changelist
    for i in range(1, 10):
        for j in range(i + 1, 10):
            now = copy.deepcopy(nowlist)
            swap = [i, j]
            now = swaplist(now, swap)
            if judge(now,endlist):
                d = get_fn(now, endlist)
                if d < min:
                    min = d
                    row = i
                    col = j
            else:
                continue
    return swaplist(nowlist, [row, col]),row,col

# 状态节点
class State(object):
    def __init__(self, gn=0, hn=0, state=None, hash_value=None, par=None, dirt=None):
        '''
        初始化
        :param gn: gn是初始化到现在的距离
        :param hn: 启发距离
        :param state: 节点存储的状态
        :param hash_value: 哈希值，用于判重
        :param par: 父节点指针
        '''
        self.dirt = dirt
        self.gn = gn
        self.hn = hn
        self.fn = self.gn + self.hn
        self.child = []  # 孩子节点
        self.par = par  # 父节点
        self.state = state  # 局面状态
        self.hash_value = hash_value  # 哈希值
        self.swaplist = []
    def __lt__(self, other):  # 用于堆的比较，返回距离最小的
        return self.fn < other.fn

    def __eq__(self, other):  # 相等的判断
        return self.hash_value == other.hash_value

    def __ne__(self, other):  # 不等的判断
        return not self.__eq__(other)
    def setswap(self, swaplist):
        self.swaplist = swaplist

def manhattan_dis(cur_node, end_node):
    '''
    计算曼哈顿距离
    :param cur_state: 当前状态
    :return: 到目的状态的曼哈顿距离
    '''
    cur_state = cur_node.state
    end_state = end_node.state
    dist = 0
    N = len(cur_state)
    for i in range(N):
        for j in range(N):
            if cur_state[i][j] == end_state[i][j]:
                continue
            num = cur_state[i][j]
            if num == 0:
                x = N - 1
                y = N - 1
            else:
                x = num / N  # 理论横坐标
                y = num - N * x - 1  # 理论的纵坐标
            dist += (abs(x - i) + abs(y - j))

    return dist


def generate_child(cur_node, end_node, hash_set, open_table, dis_fn):
    '''
    生成子节点函数
    :param cur_node:  当前节点
    :param end_node:  最终状态节点
    :param hash_set:  哈希表，用于判重
    :param open_table: OPEN表
    :param dis_fn: 距离函数
    :return: None
    '''
    if cur_node == end_node:
        heapq.heappush(open_table, end_node)
        return
    num = len(cur_node.state)
    for i in range(0, num):
        for j in range(0, num):
            if cur_node.state[i][j] != 0:
                continue
            for d in direction:  # 四个偏移方向
                x = i + d[0]
                y = j + d[1]
                if d[0] == 0 and d[1] == -1:
                    dir = 'a'
                if d[0] == 0 and d[1] == 1:
                    dir = 'd'
                if d[0] == 1 and d[1] == 0:
                    dir = 's'
                if d[0] == -1 and d[1] == 0:
                    dir = 'w'
                if x < 0 or x >= num or y < 0 or y >= num:  # 越界了
                    continue
                # 记录扩展节点的个数
                global SUM_NODE_NUM
                SUM_NODE_NUM += 1

                state = copy.deepcopy(cur_node.state)  # 复制父节点的状态
                state[i][j], state[x][y] = state[x][y], state[i][j]  # 交换位置
                h = hash(str(state))  # 哈希时要先转换成字符串
                if h in hash_set:  # 重复了
                    continue
                hash_set.add(h)  # 加入哈希表
                gn = cur_node.gn + 1  # 已经走的距离函数
                hn = dis_fn(cur_node, end_node)  # 启发的距离函数
                node = State(gn, hn, state, h, cur_node, dir)  # 新建节点
                cur_node.child.append(node)  # 加入到孩子队列
                heapq.heappush(open_table, node)  # 加入到堆中


def print_path(node,step):
    '''
    输出路径
    :param node: 最终的节点
    :return: None
    '''
    num = node.gn

    #def show_block(block):
        #print("---------------")
        #for b in block:
            #print(b)

    global pathlist
    swap = []
    stack = []  # 模拟栈
    path = []
    while node.par is not None:
        if node.gn ==  step:
            swap = node.swaplist
        stack.append(node.state)
        path.append(node.dirt)
        node = node.par
    stack.append(node.state)
    while len(stack) != 0:
        t = stack.pop()
        #show_block(t)
    while len(path) != 0:
        d = path.pop()
        pathlist += str(d)
    return num,swap


def A_start(start, end, distance_fn, generate_child_fn, step, swap, k, time_limit=10):
    '''
    A*算法
    :param swap: 强制交换的块
    :param step: 强制交换的步数
    :param start: 起始状态
    :param end: 终止状态
    :param distance_fn: 距离函数，可以使用自定义的
    :param generate_child_fn: 产生孩子节点的函数
    :param time_limit: 时间限制，默认10秒
    :return: None
    '''
    root = State(0, 0, start, hash(str(START)), None)  # 根节点
    end_state = State(0, 0, end, hash(str(END)), None)  # 最后的节点

    OPEN.append(root)
    heapq.heapify(OPEN)

    node_hash_set = set()  # 存储节点的哈希值
    node_hash_set.add(root.hash_value)
    start_time = datetime.datetime.now()
    while len(OPEN) != 0:
        top = heapq.heappop(OPEN)
        if top == end_state:  # 结束后直接输出路径
            return print_path(top,step)
        # 产生孩子节点，孩子节点加入OPEN表
        if k == 0:
            if top.gn == step :
                top.state = swaplist(top.state, swap)
                if not judge(top.state, end):
                    top.state,i,j= change(top.state, end)
                    top.setswap([i,j])
        generate_child_fn(cur_node=top, end_node=end_state, hash_set=node_hash_set,
                          open_table=OPEN, dis_fn=distance_fn)
        cur_time = datetime.datetime.now()
        # 超时处理
        if (cur_time - start_time).seconds > time_limit:
            return -1
    return -1

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

def getchallenge(uuid):
    url = "http://47.102.118.1:8089/api/challenge/start/"+ uuid
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
    img_base64 = text["data"]["img"]
    step = text["data"]["step"]
    swap = text["data"]["swap"]
    uuid = text["uuid"]
    suc = text["success"]
    chance = text["chanceleft"]
    print("suc = ")
    print(suc)
    print("chance = "+str(chance))
    img = base64.b64decode(img_base64)
    # 获取接口的图片并写入本地
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
            "teamid": 21,
            "token": "a8aee99c-f29b-42c6-abd0-72216d8d851c",
            "answer": {
                "operations": operations,
                "swap": swap}}
        )
        r=requests.post(url,headers = headers,data = data_json)
        print(r.text)

def cutimage():
    # 切割图片
    img = Image.open('photo.jpg')
    size = img.size
    # 准备将图片切割成9张小图片
    weight = int(size[0] // 3)
    height = int(size[1] // 3)
    # 切割后的小图的宽度和高度

    for j in range(3):
        for i in range(3):
            box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
            region = img.crop(box)
            region.save('{}{}.jpg'.format(j, i))

def compare(pic1,pic2):
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))

    if differ == 0:
        return True
    else:
        return False

#获得图片所对应的图是哪一区域
def getnum(path11):
    path = 'E://PyCharm 2020.2.1//python//确定序列//'
    for i in range(0, 36):
        path2 = path + str(i) + '_'
        for j in range(1, 10):
            path22 = path2 + str(j) + '.jpg'
            if compare(path11, path22):
                return i

def bulitlist(num):
    list1 = []
    for i in range(3):
        for j in range(3):
            path1 = 'E://PyCharm 2020.2.1//python//' + str(i) + str(j) + '.jpg'
            if compare(path1, 'E://PyCharm 2020.2.1//python//确定序列//white.jpg'):
                list1.append(0)
            else:
                for k in range(1, 10):
                    path2 = 'E://PyCharm 2020.2.1//python//确定序列//' + str(num) + '_' + str(k) + '.jpg'
                    if compare(path1, path2):
                        list1.append(k)
    sum = 0
    for i in list1:
        sum += i
    whitenum = 45-sum
    list2 = [[], [], []]
    list2[0] = list1[0:3]
    list2[1] = list1[3:6]
    list2[2] = list1[6:9]
    return list2,whitenum

def getlist():
    path11 = ''
    for i in range(0, 3):
        for j in range(0, 3):
            filename = 'E://PyCharm 2020.2.1//python//' + str(i) + str(j) + ".jpg"
            if not compare(filename, 'E://PyCharm 2020.2.1//python//确定序列//white.jpg'):
                if not compare(filename, 'E://PyCharm 2020.2.1//python//确定序列//black.jpg'):
                    path11 = filename
                    break
    num = getnum(path11)
    nowlist = bulitlist(num)
    return nowlist

def getendlist(num,orilist):
    num -= 1
    orilist[num//3][num%3] = 0
    return orilist

if __name__ == '__main__':
    step, swap, uuid = getchallenge("eb1efa71-b0a5-4410-8c94-343130ea7ed8")
    cutimage()
    orilist = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    nowlist, num = getlist()
    endlist = getendlist(num, orilist)
    OPEN = []  # 这里别忘了清空
    START = nowlist
    END = endlist
    k = 0
    myswap = []

    if step == 0:
        k = 1
        START = swaplist(START, swap)
        if not judge(START,END):
            START, i, j = change(START, END)
            myswap = [i,j]

    if judge(START, END):
        length, myswap = A_start(START, END, manhattan_dis, generate_child, step, swap, k, time_limit=10)
        if length != -1:
            print("length =", length)
            print("myswap =", myswap)
    else :
        START = getswaplist(START, step )
        k = 1
        START = swaplist(START, swap)
        if not judge(START,END):
            START, i, j = change(START, END)
            myswap = [i,j]
        length,myswap_ = A_start(START, END, manhattan_dis, generate_child, step, swap, k, time_limit=10)
        if myswap == []:
            myswap = myswap_
        if length != -1:
            print("length =", length + step)
            print("myswap =", myswap)
    print(uuid)
    print("step = ",step)
    print("swap = ",swap)
    print(pathlist)
    postAnswer(uuid, pathlist, myswap)



