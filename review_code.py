"""
验证代码是否解决相应突发事件
"""

import os
import json
import re
import time
import importlib.util
import multiprocessing
import pandas as pd
from tqdm import tqdm

# --- 配置 ---
TIMEOUT = 5  # 单个文件运行超时时间

# --- 验证逻辑核心 ---
class DynamicVerifier:
    """验证器"""
    def __init__(self, module):
        self.module = module

    def check_truck_interval(self, text):
        """验证: 从第X辆货车开始间隔改为Y分钟"""
        match = re.search(r"从第(\d+)辆货车开始间隔改为(\d+)分钟", text)
        if not match:
            return False
        start_idx = int(match.group(1))-1 if int(match.group(1)) > 0 else 0
        new_interval = int(match.group(2))
        try:
            trucks = self.module.init_truck_arrival_time(15)
            if start_idx + 1 >= len(trucks):
                return False
            t1 = time.mktime(time.strptime(trucks[start_idx]['arrival_time'], "%H:%M:%S"))
            t2 = time.mktime(time.strptime(trucks[start_idx + 1]['arrival_time'], "%H:%M:%S"))
            return abs((t2 - t1) - new_interval * 60) < 1
        except:
            return False

    def check_zone_stock_increase(self, text):
        """验证: Zone_X堆积区当前库存增加Y"""
        match = re.search(r"(Zone_\d+)堆积区当前库存增加(\d+)", text)
        if not match:
            return False
        target_id = match.group(1)
        increase = int(match.group(2))
        try:
            zones = self.module.init_stacking_zones()
            target = next((z for z in zones if z.get('id') == target_id), None)
            if not target:
                return False
            return target.get('current_stock', 0) == increase
        except:
            return False

    def check_zone_capacity_reduce(self, text):
        """验证: Zone_X堆积区最大容量缩减至Y"""
        match = re.search(r"(Zone_\d+)堆积区最大容量缩减至(\d+)", text)
        if not match:
            return False
        target_id = match.group(1)
        new_cap = int(match.group(2))
        try:
            zones = self.module.init_stacking_zones()
            target = next((z for z in zones if z.get('id') == target_id), None)
            if not target:
                return False
            return target.get('max_capacity') == new_cap
        except:
            return False

    def check_zone_unavailable(self, text):
        """验证: Zone_X堆积区发生故障不可用"""
        match = re.search(r"(Zone_\d+)堆积区发生故障不可用", text)
        if not match:
            return False
        target_id = match.group(1)
        try:
            zones = self.module.init_stacking_zones()
            ids = [z.get('id') for z in zones]
            return target_id not in ids
        except:
            return False

    def check_forklift_unavailable(self, text):
        """验证: Forklift_X叉车发生故障不可用"""
        match = re.search(r"(Forklift_\d+)叉车发生故障不可用", text)
        if not match:
            return False
        target_id = match.group(1)
        try:
            forklifts = self.module.init_forklifts()
            ids = [f.get('id') for f in forklifts]
            return target_id not in ids
        except:
            return False

    def check_forklift_location(self, text):
        """验证: Forklift_X叉车初始位置调整为(a,b)"""
        match = re.search(r"(Forklift_\d+)叉车初始位置调整为\((\d+),(\d+)\)", text)
        if not match:
            return False
        target_id = match.group(1)
        new_x, new_y = int(match.group(2)), int(match.group(3))
        try:
            forklifts = self.module.init_forklifts()
            target = next((f for f in forklifts if f.get('id') == target_id), None)
            if not target:
                return False
            loc = target.get('location')
            return loc == (new_x, new_y) or loc == [new_x, new_y]
        except:
            return False

    def check_route_fault(self, text):
        """验证: 站位(x,y)...四个点发生故障"""
        matches = re.findall(r"\((\d+),(\d+)\)", text)
        if len(matches) < 4:
            return False
        fault_points = [(int(x), int(y)) for x, y in matches[:4]]
        try:
            path = self.module.route_planning((0, 0), fault_points[0])
            return path is None
        except:
            return False

    def check_endpoint_change(self, text):
        """验证: 终点调整"""
        match = re.search(r"调整为\((\d+),(\d+)\)", text)
        if not match:
            return False
        new_end_x, new_end_y = int(match.group(1)), int(match.group(2))
        try:
            path = self.module.route_planning((0, 0), (new_end_x - 1, new_end_y))
            if path and list(path[-1]) == [new_end_x, new_end_y]:
                return True
            return False
        except:
            return False

def run_verify_case(file_path, emergency_list, return_dict):
    """
    单个进程运行：加载模块并验证该文件对应的特情列表
    """
    try:
        # 动态加载模块
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        verifier = DynamicVerifier(module)
        
        solved_count = 0
        unsolved = []

        for event in emergency_list:
            is_solved = False

            if "间隔改为" in event:
                is_solved = verifier.check_truck_interval(event)
            elif "库存增加" in event:
                is_solved = verifier.check_zone_stock_increase(event)
            elif "容量缩减" in event:
                is_solved = verifier.check_zone_capacity_reduce(event)
            elif "堆积区发生故障不可用" in event:
                is_solved = verifier.check_zone_unavailable(event)
            elif "叉车发生故障不可用" in event:
                is_solved = verifier.check_forklift_unavailable(event)
            elif "叉车初始位置调整" in event:
                is_solved = verifier.check_forklift_location(event)
            elif "四个点发生故障" in event:
                is_solved = verifier.check_route_fault(event)
            elif "终点" in event:
                is_solved = verifier.check_endpoint_change(event)
            
            if is_solved:
                solved_count += 1
            else:
                unsolved.append(event)

        return_dict['result'] = {
            'total': len(emergency_list),
            'solved': solved_count,
            'unsolved': unsolved,
        }
        
    except Exception as e:
        return_dict['error'] = str(e)

def main(DATASET_FILE, RESULT_DIR):
    # 1. 读取生成的特情数据
    with open(DATASET_FILE, 'r', encoding='utf-8') as f:
        dataset = json.load(f)

    # 2. 准备文件列表
    files = sorted([f for f in os.listdir(RESULT_DIR) if f.startswith('result_') and f.endswith('.py')],
                   key=lambda x: int(x.split('_')[1].split('.')[0]))

    total_emergencies_all = 0
    total_solved_all = 0
    
    file_stats = []

    print(f"开始测试 {len(files)} 个文件，对照 {len(dataset)} 条生成的特情数据...")
    print("-" * 60)

    for filename in tqdm(files):
        dataset_idx = int(filename.split('_')[1].split('.')[0]) - 1
        if dataset_idx >= len(dataset) or dataset_idx < 0:
            continue

        situation_str = dataset[dataset_idx].get("emergency_situation", "")
        # 分割成独立的事件列表
        events = [e.strip() for e in situation_str.split(';') if e.strip()]
        
        file_path = os.path.join(RESULT_DIR, filename)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        
        # 启动进程运行测试
        p = multiprocessing.Process(target=run_verify_case, args=(file_path, events, return_dict))
        p.start()
        p.join(TIMEOUT)
        
        if p.is_alive():
            p.terminate()
            p.join()
            res = {'total': len(events), 'solved': 0, 'status': '超时'}
            print(f"[超时] {filename}")
        elif 'error' in return_dict:
            res = {'total': len(events), 'solved': 0, 'status': '报错'}
            print(f"[报错] {filename}: {return_dict['error']}")
        else:
            data = return_dict.get('result', {'total': 0, 'solved': 0, 'unsolved': []})
            res = {'total': data['total'], 'solved': data['solved'], 'status': '正常'}
            if data['unsolved']:
                print(f"[未完全解决] {filename}: {data['solved']}/{data['total']}")
                for ev in data['unsolved']:
                    print(f"  未解决: {ev}")

        total_emergencies_all += res['total']
        total_solved_all += res['solved']
        
        file_stats.append({
            "文件名": filename,
            "特情总数": res['total'],
            "解决数量": res['solved'],
            "状态": res['status']
        })

    # --- 输出报告 ---
    df = pd.DataFrame(file_stats)
    
    print("\n" + "="*30 + " 最终统计结果 " + "="*30)
    print(f"测试文件数量: {len(df)}")
    print(f"一共生成的特情总数: {total_emergencies_all}")
    print(f"一共解决的特情总数: {total_solved_all}")
    if total_emergencies_all > 0:
        print(f"整体解决率: {total_solved_all / total_emergencies_all:.2%}")
    else:
        print("整体解决率: 0%")
    print("="*76)
    return total_solved_all / total_emergencies_all

if __name__ == "__main__":
    RESULT_DIR = '/root/code/neuralcomputing/datasets/glm5'
    DATASET_FILE = '/root/code/neuralcomputing/datasets/decision_raw_train_datas.json'
    main(DATASET_FILE, RESULT_DIR)