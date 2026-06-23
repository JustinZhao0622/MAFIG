import heapq
import time
import random

def route_planning(...):
    ...
    if end_point == (7,8):
        end_point = (8,8)
    ...

但这样可能会影响其他调用，但根据突发事件描述，只有该点故障，所以这样处理是正确的。

第三个问题：四个故障点。需要修改route_planning函数，使其在探索路径时避开这些点。因此，在检查下一个点是否在网格范围内后，还需要检查是否是故障点。例如，在循环中，当生成next_pos后，检查是否在故障点集合中，如果是，则跳过。因此，在函数内部定义故障点集合：

faulty_points = {(6,4), (7,4), (6,5), (7,5)}

然后，在生成next_pos后，检查是否在faulty_points中，如果是，则跳过。

现在，将这些修改整合到代码中。

需要注意的是，不能修改函数名、参数列表、返回值形式，也不能添加或删除import语句。因此，所有修改必须在原有函数内部进行。

现在，逐个修改：

1. 修改init_cranes函数中的duration和时间：

原代码：

vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})

修改为：

if i == 2:
    duration = 20
else:
    duration = 10
vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})

同时，处理第4艘船的延迟：

vessel_time = time.strftime(...) 的时间戳是 time.mktime(start_time) + 3*60*i + (10*60 if i ==3 else 0)

所以，修改vessel_time的计算：

vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i + (10 * 60 if i == 3 else 0)))

2. 修改route_planning函数：

在函数开始处，检查end_point是否为(7,8)，如果是，则改为(8,8)。然后，在生成next_pos后，检查是否在故障点集合中，如果是，则跳过。

所以，在函数内部：

def route_planning(...):
    ...
    # 检查终点是否为故障点
    if end_point == (7,8):
        end_point = (8,8)
    # 定义故障点集合
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}
    ...
    # 在生成next_pos后检查是否在故障点
    if next_pos in faulty_points:
        continue

这样处理是否正确？

是的，这样就能避开故障点。

现在，将这些修改应用到代码中。

需要注意的是，原代码中的route_planning函数中的directions是四个方向，可能需要确保路径规划不会经过故障点。

综上，修改后的代码如下：

在init_cranes函数中，修改duration和时间计算。

在route_planning函数中，处理终点调整和故障点避开。

现在，将这些修改整合到代码中，确保不违反任何规则。
</think>

"""
原子函数库
"""


 

def init_cranes(nums=5,start_time="8:00:00"):
    """初始化船舶，每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i + (10 * 60 if i == 3 else 0)))
        duration = 20 if i == 2 else 10
        vessels.append({"time": vessel_time, "id": i, "duration": duration, "location": (i,10)})
    return vessels

def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources

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

    # 检查终点是否为故障点
    if end_point == (7,8):
        end_point = (8,8)

    # 定义故障点集合
    faulty_points = {(6,4), (7,4), (6,5), (7,5)}

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

            # 检查是否为故障点
            if next_pos in faulty_points:
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


def init_trucks(nums=8):
    """初始化集卡车队，返回车辆列表，每辆车包含id、位置、状态"""
    trucks = []
    for i in range(nums):
        trucks.append({
            "id": f"Truck_{i+1}",
            "location": (random.randint(0, 20), random.randint(0, 20)),
            "status": "idle",
        })
    return trucks


def init_yard_blocks(nums=6):
    """初始化堆场区块，返回区块列表，每个区块包含id、容量、当前占用"""
    yard_blocks = []
    for i in range(nums):
        yard_blocks.append({
            "id": f"Block_{i+1}",
            "capacity": 100,
            "occupied": random.randint(0, 60),
        })
    return yard_blocks


def init_berths(nums=4):
    """初始化泊位，返回泊位列表，每个泊位包含id、位置、状态"""
    berths = []
    for i in range(nums):
        berths.append({
            "id": f"Berth_{i+1}",
            "location": (i * 10, 0),
            "status": "available",
        })
    return berths


def init_containers(nums=12):
    """初始化集装箱，返回集装箱列表，每个集装箱包含id、位置、类型"""
    containers = []
    for i in range(nums):
        containers.append({
            "id": f"Container_{i+1}",
            "location": (random.randint(0, 10), random.randint(0, 10)),
            "type": "general",
        })
    return containers


def init_loading_tasks(nums=10):
    """初始化装卸任务，返回任务列表，每个任务包含id、目标资源、状态"""
    loading_tasks = []
    for i in range(nums):
        loading_tasks.append({
            "id": f"Task_{i+1}",
            "target": f"Container_{(i % 12) + 1}",
            "status": "waiting",
        })
    return loading_tasks
