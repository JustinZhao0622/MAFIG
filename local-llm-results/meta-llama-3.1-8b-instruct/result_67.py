import heapq
import time

# 货车到达时间
def init_truck_arrival_time(nums=10, start_time="8:00:00"):
    """
    初始化货车到达时间。货车到达的间隔时间是3分钟
    返回货车列表，每个货车包含id和到达时间
    """
    start_time = time.strptime(start_time, "%H:%M:%S")
    trucks = []
    for i in range(nums):
        arrival_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        trucks.append({
            "id": f"Truck_{i}",
            "arrival_time": arrival_time,
        })
    return trucks

def init_stacking_zones(nums=4):
    """
    初始化货物堆积区域 (A, B, C, D 区)。
    每个区域包含：坐标、当前存放数量 (current_stock)、最大容量 (max_capacity)。
    返回可用区域列表，每个区域包含id、坐标、当前存放数量、最大容量、描述
    """
    zones = []
    for i in range(nums):
        if i == 2:  # Zone_3堆积区当前库存增加41
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 41,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
        else:
            zones.append({
                "id": f"Zone_{i+1}",
                "location": (0,25),
                "current_stock": 0,
                "max_capacity": 100,
                "desc": f"货物堆积区域{i+1}"
            })
    return zones

def init_forklifts(nums=3):
    """
    初始化叉车队。
    返回可用叉车列表，每个叉车包含id、坐标
    """
    forklifts = []
    for i in range(nums):
        if i == 1:  # Forklift_2叉车初始位置调整为(45,25)
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (45, 25),
            })
        else:
            forklifts.append({
                "id": f"Forklift_{i+1}",
                "location": (0, 25),
            })
    return forklifts

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)

    参数:
        begin_point: 起点坐标 (x, y)
        end_point: 终点坐标 (x, y)
        grid_size: 地图大小 (width, height)，默认 (100, 100)

    返回:
        包含路径点的列表，每个点为 (x, y) 元组，从起点到终点
        如果没有路径则返回 None
    """
    width, height = grid_size

    # 曼哈顿距离启发式函数
    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])

    # 四个方向：上、下、左、右
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # 优先队列：(f值, 计数器, 当前点, 路径)
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)

        # 到达终点
        if current == end_point:
            return path

        # 探索四个方向
        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            # 检查是否在网格范围内
            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            # 检查是否已访问
            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1  # 实际代价
            f_score = g_score + heuristic(next_pos)  # 总评估代价

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None

def init_a():
    """初始化a"""
    a = 1
    return a

def init_b():
    """初始化b"""
    b = 2
    return b

def init_c():
    """初始化c"""
    c = 3
    return c    

def init_d():
    """初始化d"""
    d = 4
    return d
    
def init_e():
    """初始化e"""
    e = 5
    return e

def init_f():
    """初始化f"""
    f = 6
    return f
    
def init_g():
    """初始化g"""
    g = 7
    return g

def init_h():
    """初始化h"""
    h = 8
    return h
    
def init_i():
    """初始化i"""
    i = 9
    return i

def init_j():
    """初始化j"""
    j = 10
    return j
    
def init_k():
    """初始化k"""
    k = 11
    return k

def init_l():
    """初始化l"""
    l = 12
    return l
    
def init_m():
    """初始化m"""
    m = 13
    return m

def init_n():
    """初始化n"""
    n = 14
    return n
    
def init_o():
    """初始化o"""
    o = 15
    return o

def init_p():
    """初始化p"""
    p = 16
    return p

def init_q():
    """初始化q"""
    q = 17
    return q

def init_r():
    """初始化r"""
    r = 18
    return r

def init_s():
    """初始化s"""
    s = 19
    return s

def init_t():
    """初始化t"""
    t = 20
    return t

def init_u():
    """初始化u"""
    u = 21
    return u

def init_v():
    """初始化v"""
    v = 22
    return v

def init_w():
    """初始化w"""
    w = 23
    return w

def init_x():
    """初始化x"""
    x = 24
    return x

def init_y():
    """初始化y"""
    y = 25
    return y

def init_z():
    """初始化z"""
    z = 26
    return z

def init_aa():
    """初始化aa"""
    aa = 27
    return aa

def init_bb():
    """初始化bb"""
    bb = 28
    return bb

def init_cc():
    """初始化cc"""
    cc = 29
    return cc

def init_dd():
    """初始化dd"""
    dd = 30
    return dd

def init_ee():
    """初始化ee"""
    ee = 31
    return ee

def init_ff():
    """初始化ff"""
    ff = 32
    return ff

def init_gg():
    """初始化gg"""
    gg = 33
    return gg

def init_hh():
    """初始化hh"""
    hh = 34
    return hh

def init_ii():
    """初始化ii"""
    ii = 35
    return ii

def init_jj():
    """初始化jj"""
    jj = 36
    return jj

def init_kk():
    """初始化kk"""
    kk = 37
    return kk

def init_ll():
    """初始化ll"""
    ll = 38
    return ll

def init_mm():
    """初始化mm"""
    mm = 39
    return mm

def init_nn():
    """初始化nn"""
    nn = 40
    return nn

def init_oo():
    """初始化oo"""
    oo = 41
    return oo

def init_pp():
    """初始化pp"""
    pp = 42
    return pp

def init_qq():
    """初始化qq"""
    qq = 43
    return qq

def init_rr():
    """初始化rr"""
    rr = 44
    return rr

def init_ss():
    """初始化ss"""
    ss = 45
    return ss

def init_tt():
    """初始化tt"""
    tt = 46
    return tt

def init_uu():
    """初始化uu"""
    uu = 47
    return uu

def init_vv():
    """初始化vv"""
    vv = 48
    return vv

def init_ww():
    """初始化ww"""
    ww = 49
    return ww

def init_xx():
    """初始化xx"""
    xx = 50
    return xx

def init_yy():
    """初始化yy"""
    yy = 51
    return yy

def init_zz():
    """初始化zz"""
    zz = 52
    return zz

def init_aaaa():
    """初始化aaaa"""
    aaaa = 53
    return aaaa

def init_bbbb():
    """初始化bbbbb"""
    bbbb = 54
    return bbbb

def init_cccc():
    """初始化ccccc"""
    cccc = 55
    return cccc

def init_dddd():
    """初始化ddddd"""
    dddd = 56
    return dddd

def init_eeeee():
    """初始化eeeee"""
    eeeee = 57
    return eeeee

def init_fffff():
    """初始化fffff"""
    fffff = 58
    return fffff

def init_ggggg():
    """初始化ggggg"""
    ggggg = 59
    return ggggg

def init_hhhhh():
    """初始化hhhhh"""
    hhhhh = 60
    return hhhhh

def init_iiiiii():
    """初始化iiiiii"""
    iiii = 61
    return iiii

def init_jjjjjj():
    """初始化jjjjjj"""
    jjjjj = 62
    return jjjjj

def init_kkkkkk():
    """初始化kkkkkk"""
    kkkkk = 63
    return kkkkk

def init_llllll():
    """初始化llllll"""
    lllll = 64
    return lllll

def init_mmmmmm():
    """初始化mmmmmm"""
    mmmmm = 65
    return mmmmm

def init_nnnnnn():
    """初始化nnnnnn"""
    nnnnn = 66
    return nnnnn

def init_oooooo():
    """初始化oooooo"""
    ooooo = 67
    return ooooo

def init_pppppp():
    """初始化pppppp"""
    ppppp = 68
    return ppppp

def init_qqqqqq():
    """初始化qqqqqq"""
    qqqqq = 69
    return qqqqq

def init_rrrrrr():
    """初始化rrrrrr"""
    rrrrr = 70
    return rrrrr

def init_ssssss():
    """初始化ssssss"""
    sssss = 71
    return sssss

def init_tttttt():
    """初始化tttttt"""
    ttttt = 72
    return ttttt

def init_uuu
