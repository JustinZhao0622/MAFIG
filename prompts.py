# 原始调度函数代码
with open("functions.py", "r", encoding="utf-8") as f:
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

3. 不允许通过以下方式绕过问题：
   - 直接 return / pass 跳过核心逻辑
   - 硬编码结果
   - 删除关键调度步骤
   - 捕获异常但不处理真实冲突

【突发事件约束】
4. 突发事件描述是唯一可信事实来源
   - 不允许引入未明确给出的新故障、新延迟或新假设

【输出格式】
5. 仅返回修改后的完整 Python 代码
   - 必须包含 import 语句
   - 不允许任何解释说明
   - 不允许 markdown 代码块
   - 不允许示例、不允许多余文本
"""


USER_PROMPT = """
EMERGENCY_SITUATIONS:
{EMERGENCY_SITUATIONS}

CODE:
{ORIGINAL_CODE}

请基于上述突发事件，对代码进行必要修改。
"""


init_planes = '''
import heapq
import time
import random

def init_planes(nums=5,start_time="8:00:00"):
    """初始化舰载机，每隔三分钟到达一架舰载机，返回舰载机列表，每个舰载机包含时间、id，任务时长都为10分钟"""
    start_time = time.strptime(start_time, "%H:%M:%S")
    planes = []
    for i in range(nums):
        plane_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(start_time) + 3 * 60 * i))
        planes.append({"time": plane_time, "id": i, "duration": 10, "location": (i,10)})
    return planes
'''


init_fixed_resources = '''
import heapq
import time
import random

def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources
'''


init_mobile_resources = '''
import heapq
import time
import random

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources
'''


init_tractor_resources = '''
import heapq
import time
import random

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources
'''


init_fuel_truck_resources = '''
import heapq
import time
import random

def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources
'''


init_nitrogen_truck_resources = '''
import heapq
import time
import random

def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources
'''


init_oxygen_truck_resources = '''
import heapq
import time
import random

def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources
'''


init_power_cart_resources = '''
import heapq
import time
import random

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources
'''


init_air_source_car_resources = '''
import heapq
import time
import random

def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources
'''


init_hydraulic_cart_resources = '''
import heapq
import time
import random

def init_hydraulic_cart_resources(nums=10):
    """初始化液压车资源，返回资源列表，每个资源包含id、类型"""
    hydraulic_cart_resources = []
    for i in range(nums):
        hydraulic_cart_resources.append({"id": i, "type": "hydraulic_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_cart_resources
'''


init_maintenance_vehicle_resources = '''
import heapq
import time
import random

def init_maintenance_vehicle_resources(nums=10):
    """初始化维修车资源，返回资源列表，每个资源包含id、类型"""
    maintenance_vehicle_resources = []
    for i in range(nums):
        maintenance_vehicle_resources.append({"id": i, "type": "maintenance_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_vehicle_resources
'''


init_fire_vehicle_resources = '''
import heapq
import time
import random

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources
'''


init_towing_tasks = '''
import heapq
import time
import random

def init_towing_tasks(nums=6):
    """初始化牵引任务，返回任务列表，每个任务包含id、类型"""
    towing_tasks = []
    for i in range(nums):
        towing_tasks.append({"id": i, "type": "towing", "location": (random.randint(0, 3), random.randint(0, 10))})
    return towing_tasks
'''


init_refueling_tasks = '''
import heapq
import time
import random

def init_refueling_tasks(nums=6):
    """初始化加油任务，返回任务列表，每个任务包含id、类型"""
    refueling_tasks = []
    for i in range(nums):
        refueling_tasks.append({"id": i, "type": "refueling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return refueling_tasks
'''


init_nitrogen_filling_tasks = '''
import heapq
import time
import random

def init_nitrogen_filling_tasks(nums=6):
    """初始化加氮任务，返回任务列表，每个任务包含id、类型"""
    nitrogen_filling_tasks = []
    for i in range(nums):
        nitrogen_filling_tasks.append({"id": i, "type": "nitrogen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_filling_tasks
'''


init_oxygen_filling_tasks = '''
import heapq
import time
import random

def init_oxygen_filling_tasks(nums=6):
    """初始化充氧任务，返回任务列表，每个任务包含id、类型"""
    oxygen_filling_tasks = []
    for i in range(nums):
        oxygen_filling_tasks.append({"id": i, "type": "oxygen_filling", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_filling_tasks
'''


init_power_supply_tasks = '''
import heapq
import time
import random

def init_power_supply_tasks(nums=6):
    """初始化供电任务，返回任务列表，每个任务包含id、类型"""
    power_supply_tasks = []
    for i in range(nums):
        power_supply_tasks.append({"id": i, "type": "power_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_supply_tasks
'''


init_air_supply_tasks = '''
import heapq
import time
import random

def init_air_supply_tasks(nums=6):
    """初始化供气任务，返回任务列表，每个任务包含id、类型"""
    air_supply_tasks = []
    for i in range(nums):
        air_supply_tasks.append({"id": i, "type": "air_supply", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_supply_tasks
'''


init_hydraulic_support_tasks = '''
import heapq
import time
import random

def init_hydraulic_support_tasks(nums=6):
    """初始化液压保障任务，返回任务列表，每个任务包含id、类型"""
    hydraulic_support_tasks = []
    for i in range(nums):
        hydraulic_support_tasks.append({"id": i, "type": "hydraulic_support", "location": (random.randint(0, 3), random.randint(0, 10))})
    return hydraulic_support_tasks
'''


init_maintenance_tasks = '''
import heapq
import time
import random

def init_maintenance_tasks(nums=6):
    """初始化维修保障任务，返回任务列表，每个任务包含id、类型"""
    maintenance_tasks = []
    for i in range(nums):
        maintenance_tasks.append({"id": i, "type": "maintenance", "location": (random.randint(0, 3), random.randint(0, 10))})
    return maintenance_tasks
'''


init_inspection_tasks = '''
import heapq
import time
import random

def init_inspection_tasks(nums=6):
    """初始化检查任务，返回任务列表，每个任务包含id、类型"""
    inspection_tasks = []
    for i in range(nums):
        inspection_tasks.append({"id": i, "type": "inspection", "location": (random.randint(0, 3), random.randint(0, 10))})
    return inspection_tasks
'''


init_fire_watch_tasks = '''
import heapq
import time
import random

def init_fire_watch_tasks(nums=6):
    """初始化消防监护任务，返回任务列表，每个任务包含id、类型"""
    fire_watch_tasks = []
    for i in range(nums):
        fire_watch_tasks.append({"id": i, "type": "fire_watch", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_watch_tasks
'''


init_tasks = '''
import heapq
import time
import random

def init_tasks(nums=6):
    """初始化挂载弹药任务，返回任务列表，每个任务包含id、类型"""
    ammo_tasks = []
    for i in range(nums):
        ammo_tasks.append({"id": i, "type": "ammo", "location": (random.randint(0, 3), random.randint(0, 10))})
    return ammo_tasks
'''


route_planning = '''
import heapq
import time
import random

def route_planning(begin_point, end_point, grid_size=(100, 100)):
    """从一个点到另一个点的路径规划 (使用A*算法)"""
    width, height = grid_size

    def heuristic(pos):
        return abs(pos[0] - end_point[0]) + abs(pos[1] - end_point[1])

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    counter = 0
    heap = [(heuristic(begin_point), counter, begin_point, [begin_point])]
    visited = {begin_point}

    while heap:
        f_score, _, current, path = heapq.heappop(heap)
        if current == end_point:
            return path

        for dx, dy in directions:
            next_x = current[0] + dx
            next_y = current[1] + dy
            next_pos = (next_x, next_y)

            if not (0 <= next_x < width and 0 <= next_y < height):
                continue

            if next_pos in visited:
                continue

            visited.add(next_pos)
            new_path = path + [next_pos]
            g_score = len(new_path) - 1
            f_score = g_score + heuristic(next_pos)

            counter += 1
            heapq.heappush(heap, (f_score, counter, next_pos, new_path))
    return None
'''


functions_mapping = {
    "init_planes": init_planes,
    "init_fixed_resources": init_fixed_resources,
    "init_mobile_resources": init_mobile_resources,
    "init_tractor_resources": init_tractor_resources,
    "init_fuel_truck_resources": init_fuel_truck_resources,
    "init_nitrogen_truck_resources": init_nitrogen_truck_resources,
    "init_oxygen_truck_resources": init_oxygen_truck_resources,
    "init_power_cart_resources": init_power_cart_resources,
    "init_air_source_car_resources": init_air_source_car_resources,
    "init_hydraulic_cart_resources": init_hydraulic_cart_resources,
    "init_maintenance_vehicle_resources": init_maintenance_vehicle_resources,
    "init_fire_vehicle_resources": init_fire_vehicle_resources,
    "init_towing_tasks": init_towing_tasks,
    "init_refueling_tasks": init_refueling_tasks,
    "init_nitrogen_filling_tasks": init_nitrogen_filling_tasks,
    "init_oxygen_filling_tasks": init_oxygen_filling_tasks,
    "init_power_supply_tasks": init_power_supply_tasks,
    "init_air_supply_tasks": init_air_supply_tasks,
    "init_hydraulic_support_tasks": init_hydraulic_support_tasks,
    "init_maintenance_tasks": init_maintenance_tasks,
    "init_inspection_tasks": init_inspection_tasks,
    "init_fire_watch_tasks": init_fire_watch_tasks,
    "init_tasks": init_tasks,
    "route_planning": route_planning,
}


perception_system_prompt = """
你是一名资深的信息处理与系统诊断专家。你的任务是分析突发事件描述，并根据给定的原子函数库定义，判断该事件需要修改哪个函数来应对。

规则：一个突发事件只允许映射到一个函数。必须选择直接负责该资源、该任务或该路径逻辑的函数，不能跨函数联想。

### 原子函数库定义
1. `init_planes`
- 职责：舰载机到达时间、到达间隔、到达顺序。
- 关键词：舰载机、到达、间隔、延迟。

2. `init_fixed_resources`
- 职责：固定保障资源的位置与属性。
- 关键词：固定保障资源、固定资源、初始位置。

3. `init_mobile_resources`
- 职责：通用移动资源的位置、可用性。
- 关键词：通用移动资源、移动资源、故障、不可用。

4. `init_tractor_resources`
- 职责：牵引车资源的位置、可用性。
- 关键词：牵引车、拖车、位置调整、不可用。

5. `init_fuel_truck_resources`
- 职责：加油车资源的位置、可用性。
- 关键词：加油车、加油保障、故障、不可用。

6. `init_nitrogen_truck_resources`
- 职责：加氮车资源的位置、可用性。
- 关键词：加氮车、氮气保障、位置调整、不可用。

7. `init_oxygen_truck_resources`
- 职责：充氧车资源的位置、可用性。
- 关键词：充氧车、氧气保障、故障、不可用。

8. `init_power_cart_resources`
- 职责：供电车资源的位置、可用性。
- 关键词：供电车、电源车、位置调整、不可用。

9. `init_air_source_car_resources`
- 职责：气源车资源的位置、可用性。
- 关键词：气源车、供气车、故障、不可用。

10. `init_hydraulic_cart_resources`
- 职责：液压车资源的位置、可用性。
- 关键词：液压车、液压保障、位置调整、不可用。

11. `init_maintenance_vehicle_resources`
- 职责：维修车资源的位置、可用性。
- 关键词：维修车、维修保障、故障、不可用。

12. `init_fire_vehicle_resources`
- 职责：消防车资源的位置、可用性。
- 关键词：消防车、消防保障、位置调整、不可用。

13. `init_towing_tasks`
- 职责：牵引任务的站位与任务属性。
- 关键词：牵引任务、目标站位、改派、调整。

14. `init_refueling_tasks`
- 职责：加油任务的站位与优先级。
- 关键词：加油任务、优先执行、站位调整。

15. `init_nitrogen_filling_tasks`
- 职责：加氮任务的站位与任务属性。
- 关键词：加氮任务、目标站位、调整。

16. `init_oxygen_filling_tasks`
- 职责：充氧任务的站位与任务属性。
- 关键词：充氧任务、改派、站位。

17. `init_power_supply_tasks`
- 职责：供电任务的站位与任务属性。
- 关键词：供电任务、目标站位、调整。

18. `init_air_supply_tasks`
- 职责：供气任务的站位与任务属性。
- 关键词：供气任务、改派、站位。

19. `init_hydraulic_support_tasks`
- 职责：液压保障任务的站位与任务属性。
- 关键词：液压保障任务、目标站位、调整。

20. `init_maintenance_tasks`
- 职责：维修保障任务的优先级与任务属性。
- 关键词：维修保障任务、优先执行、维修任务。

21. `init_inspection_tasks`
- 职责：检查任务的站位与任务属性。
- 关键词：检查任务、目标站位、调整。

22. `init_fire_watch_tasks`
- 职责：消防监护任务的站位与任务属性。
- 关键词：消防监护任务、改派、站位。

23. `init_tasks`
- 职责：挂载弹药任务的站位与任务属性。
- 关键词：挂载弹药任务、弹药任务、目标站位、调整。

24. `route_planning`
- 职责：路径规划、障碍点绕行、终点调整。
- 关键词：站位故障、路径、终点调整、不可达、route。

### 输出格式
突发事件按照;分隔，有 N 个独立事件。你必须按事件顺序输出一个 Python 列表，第 i 个元素对应第 i 个事件需要修改的函数名。
如果第 i 个突发事件无需更改，你直接在列表中添加 "None"。
只输出列表，禁止解释或其他文本。
"""


perception_user_prompt = """
突发事件：
{EMERGENCY_SITUATIONS}
本次事件共{nums}件，你只需要输出包含{nums}个函数名列表，第i个元素对应第i个事件需要修改的函数名。
"""
