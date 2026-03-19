基于突发事件的描述，需要修改以下几个函数：

1. `init_fixed_resources`：调整第2个固定保障资源初始位置为(2,1)
2. `init_tractor_resources`：调整第2辆牵引车初始位置为(3,3)
3. `init_power_cart_resources`：调整第2辆供电车初始位置为(1,10)
4. `init_fire_vehicle_resources`：调整第2辆消防车初始位置为(1,9)
5. `init_mobile_resources`：第2个通用移动资源发生故障不可用

以下是修改后的代码：


def init_fixed_resources(nums=10):
    """初始化固定资源，返回固定资源列表，每个资源包含id、类型"""
    fixed_resources = []
    for i in range(nums):
        if i == 1:  # 第2个固定保障资源初始位置调整为(2,1)
            fixed_resources.append({"id": i, "type": "crane", "location": (2, 1)})
        else:
            fixed_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fixed_resources

def init_tractor_resources(nums=10):
    """初始化牵引车资源，返回资源列表，每个资源包含id、类型"""
    tractor_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆牵引车初始位置调整为(3,3)
            tractor_resources.append({"id": i, "type": "tractor", "location": (3, 3)})
        else:
            tractor_resources.append({"id": i, "type": "tractor", "location": (random.randint(0, 3), random.randint(0, 10))})
    return tractor_resources

def init_power_cart_resources(nums=10):
    """初始化供电车资源，返回资源列表，每个资源包含id、类型"""
    power_cart_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆供电车初始位置调整为(1,10)
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (1, 10)})
        else:
            power_cart_resources.append({"id": i, "type": "power_cart", "location": (random.randint(0, 3), random.randint(0, 10))})
    return power_cart_resources

def init_fire_vehicle_resources(nums=10):
    """初始化消防车资源，返回资源列表，每个资源包含id、类型"""
    fire_vehicle_resources = []
    for i in range(nums):
        if i == 1:  # 第2辆消防车初始位置调整为(1,9)
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (1, 9)})
        else:
            fire_vehicle_resources.append({"id": i, "type": "fire_vehicle", "location": (random.randint(0, 3), random.randint(0, 10))})
    return fire_vehicle_resources

def init_mobile_resources(nums=10):
    """初始化移动资源，返回移动资源列表，每个资源包含id、类型"""
    mobile_resources = []
    for i in range(nums):
        if i == 1:  # 第2个通用移动资源发生故障不可用
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10)), "status": "故障"})
        else:
            mobile_resources.append({"id": i, "type": "crane", "location": (random.randint(0, 3), random.randint(0, 10))})
    return mobile_resources


以上修改仅在指定的函数中进行了必要的调整，其他函数保持不变。
