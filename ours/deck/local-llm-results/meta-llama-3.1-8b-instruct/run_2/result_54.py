基于突发事件的描述，第4辆供电车初始位置调整为(2,4);第4辆加油车发生故障不可用;第4辆充氧车发生故障不可用;第4辆气源车发生故障不可用;第4辆加氮车初始位置调整为(1,10);第4辆牵引车初始位置调整为(2,2)。我们需要修改以下函数：

- init_power_cart_resources
- init_fuel_truck_resources
- init_oxygen_truck_resources
- init_air_source_car_resources
- init_nitrogen_truck_resources
- init_tractor_resources

我们需要在这些函数中修改资源的初始位置和状态。


def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 3:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (2, 4), "status": "故障"})  # 第4辆供电车发生故障
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources


def init_fuel_truck_resources(nums=10):
    """初始化加油车资源，返回资源列表，每个资源包含id、类型"""
    fuel_truck_resources = []
    for i in range(nums):
        if i == 3:
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": None, "status": "故障"})  # 第4辆加油车发生故障
        else:
            fuel_truck_resources.append({"id": i, "type": "fuel_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fuel_truck_resources


def init_oxygen_truck_resources(nums=10):
    """初始化充氧车资源，返回资源列表，每个资源包含id、类型"""
    oxygen_truck_resources = []
    for i in range(nums):
        if i == 3:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": None, "status": "故障"})  # 第4辆充氧车发生故障
        else:
            oxygen_truck_resources.append({"id": i, "type": "oxygen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return oxygen_truck_resources


def init_air_source_car_resources(nums=10):
    """初始化气源车资源，返回资源列表，每个资源包含id、类型"""
    air_source_car_resources = []
    for i in range(nums):
        if i == 3:
            air_source_car_resources.append({"id": i, "type": "air_source_car", "location": None, "status": "故障"})  # 第4辆气源车发生故障
        else:
            air_source_car_resources.append({"id": i, "type": "air_source_car", "location": (random.randint(0, 3), random.randint(0, 10))})
    return air_source_car_resources


def init_nitrogen_truck_resources(nums=10):
    """初始化加氮车资源，返回资源列表，每个资源包含id、类型"""
    nitrogen_truck_resources = []
    for i in range(nums):
        if i == 3:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (1, 10)})  # 第4辆加氮车初始位置调整为(1,10)
        else:
            nitrogen_truck_resources.append({"id": i, "type": "nitrogen_truck", "location": (random.randint(0, 3), random.randint(0, 10))})
    return nitrogen_truck_resources


def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 3:
            tractor_resources.append({"id": i, "type": "tractor", "location": (2, 2)})  # 第4辆牵引车初始位置调整为(2,2)
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources


以上修改后，代码可以正确处理突发事件。
