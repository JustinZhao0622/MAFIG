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

    def check_aircraft_delay(self, text):
        """验证: Aircraft_X舰载机延迟Y分钟到达"""
        match = re.search(r"(Aircraft_\d+)舰载机延迟(\d+)分钟", text)
        if not match:
            return False
        target_id = match.group(1)
        delay_min = int(match.group(2))
        idx = int(target_id.split("_")[1])
        try:
            aircrafts = self.module.init_aircraft_arrival(15)
            target = next((a for a in aircrafts if a.get('id') == target_id), None)
            if not target:
                return False
            correct_time = time.strftime(
                "%H:%M:%S",
                time.localtime(time.mktime(time.strptime("8:00:00", "%H:%M:%S")) + 3 * 60 * idx + delay_min * 60),
            )
            return target['arrival_time'] == correct_time
        except:
            return False

    def check_fixed_resource_unavailable(self, text):
        """验证: FixedRes_X固定资源损坏不可用"""
        match = re.search(r"(FixedRes_\d+)固定资源损坏不可用", text)
        if not match:
            return False
        target_id = match.group(1)
        try:
            resources = self.module.init_fixed_resources()
            ids = [r.get('id') for r in resources]
            return target_id not in ids
        except:
            return False

    def check_mobile_resource_unavailable(self, text):
        """验证: Tractor_X牵引车损坏不可用"""
        match = re.search(r"(Tractor_\d+)牵引车损坏不可用", text)
        if not match:
            return False
        target_id = match.group(1)
        try:
            resources = self.module.init_mobile_resources()
            ids = [r.get('id') for r in resources]
            return target_id not in ids
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

            if "舰载机延迟" in event:
                is_solved = verifier.check_aircraft_delay(event)
            elif "固定资源损坏不可用" in event:
                is_solved = verifier.check_fixed_resource_unavailable(event)
            elif "牵引车损坏不可用" in event:
                is_solved = verifier.check_mobile_resource_unavailable(event)
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