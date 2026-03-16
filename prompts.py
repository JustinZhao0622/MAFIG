# 原始调度函数代码
with open('functions.py', 'r', encoding='utf-8') as f:
    ORIGINAL_CODE = f.read()


SYSTEM_PROMPT = """
你是一名【突发事件应对与调度系统重构专家】，专门负责在给定突发事件约束下，
对既有调度代码进行【最小必要修改】，以恢复系统的可运行性与逻辑一致性。

你必须严格遵守以下所有规则，任何一条违反都视为失败：

【任务目标】
- 基于给定的突发事件描述，仅对现有代码中的逻辑进行必要调整
- 使系统在当前突发条件下可以正确执行，不允许规避问题或简化处理

【修改范围与限制】
1. 只能修改【已有函数的函数体内部逻辑】  
   - 严禁新增函数  
   - 严禁删除函数  
   - 严禁修改函数名、参数列表、返回值形式  

2. 严禁修改、删除或新增任何 import 语句  
   - 必须从原始代码中原样复制 import 部分  

3. 不允许通过以下方式“绕过”问题：
   - 直接 return / pass 跳过核心逻辑
   - 硬编码结果
   - 删除关键调度步骤
   - 捕获异常但不处理真实冲突

【突发事件约束】
4. 突发事件描述是【唯一可信事实来源】  
   - 不允许引入任何未明确给出的新故障、新延迟或新假设  
   - 不允许“合理推测”额外事件  

【输出格式（极其重要）】
5. 仅返回【修改后的完整 Python 代码】
   - 必须包含 import 语句
   - 不允许任何解释说明！！！
   - 不允许 markdown 代码块（如 ```python）
   - 不允许示例、不允许注释、不允许多余文本

只输出可以被 Python 解释器直接执行的代码，你必须再三确认你的代码是不存在bug的，不允许任何多余的文本！！！
"""

USER_PROMPT = """
EMERGENCY_SITUATIONS:
{EMERGENCY_SITUATIONS}

CODE:
{ORIGINAL_CODE}

请基于上述突发事件，对代码进行必要修改。
"""

# 初始的函数
init_cranes =  '''
import heapq
import time
import random 
def init_cranes(nums=5,start_time="8:00:00"):
    """每隔三分钟到达一艘船舶，返回船舶列表，每个船舶包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    vessels = []
    for i in range(nums):
        vessel_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        vessels.append({"time": vessel_time, "id": i, "duration": 10, "location": (i,10)})
    return vessels
'''

init_resources = '''
import heapq
import time
import random 
def init_resources(nums=10):
    """初始化资源，返回可用资源列表，每个资源包含id、类型"""
    resources = []
    for i in range(nums):
        resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return resources
'''

route_planning = '''
import heapq
import time
import random 
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
'''
functions_mapping = {
    "init_cranes": init_cranes,
    "init_resources": init_resources,
    "route_planning": route_planning
}

# 感知智能体
perception_system_prompt = """
你是一名资深的信息处理与系统诊断专家。你的任务是分析“突发事件描述”，并根据给定的“原子函数库”定义，判断该事件需要修改哪个函数来应对。

### 1. 原子函数库定义
你拥有以下三个核心函数的逻辑权限：

1.  **`init_cranes`**: 
    * **职责**: 负责船舶（vessels）的初始化生成。
    * **管理属性**: 船舶到达时间（time）、船舶ID、任务时长（duration）、船舶列表生成。
    * **相关关键词**: 船舶、到达、延迟、任务时长、vessel。

2.  **`init_resources`**: 
    * **职责**: 负责岸桥/场桥等资源（resources）的初始化。
    * **管理属性**: 资源ID、资源类型、资源可用性、资源初始位置。
    * **相关关键词**: 资源、不可用、损坏、resource、id。

3.  **`route_planning`**: 
    * **职责**: 负责路径规划与地图逻辑。
    * **管理属性**: 起点、终点、障碍物（故障点）、网格地图（Grid）、A*算法逻辑。
    * **相关关键词**: 站位、故障点、坐标、路径、终点调整、不可达、route。

### 2. 输出格式（必须严格遵守）
突发事件按分号(;)分隔，有N个独立事件。你必须按事件顺序输出一个Python列表，第i个元素对应第i个事件需要修改的函数名。
如果第i个突发事件无需更改，你直接在列表中添加None，例如输入有3个事件，输出示例：["init_resources", "None", "init_cranes"]
只输出列表，禁止Markdown、解释或其他任何废话。
"""

perception_user_prompt = """
突发事件：
{EMERGENCY_SITUATIONS}
本次事件共{nums}件，你必须输出{nums}个函数名列表，第i个元素对应第i个事件需要修改的函数名。
"""
