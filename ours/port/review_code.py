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
        """初始化"""
        self.module = module

    def check_resource_unavailable(self, text):
        """验证: id为X的资源不可用"""
        # 正则提取ID: "id为3的资源不可用"
        match = re.search(r"id为(\d+)的资源", text)
        if not match: return False
        
        target_id = int(match.group(1))
        
        try:
            # 运行 init_resources 函数
            resources = self.module.init_resources(15) # 生成足够多资源以确保覆盖随机ID
            # 验证: 结果中不应包含 target_id
            ids = [r.get('id') for r in resources]
            return target_id not in ids
        except:
            return False

    def check_vessel_delay(self, text):
        """验证: 第X艘到达的船舶延迟10分钟"""
        match = re.search(r"第(\d+)艘", text)
        if not match: return False
        
        idx = int(match.group(1))-1 if int(match.group(1)) != 0 else 0
        
        try:
            objs = self.module.init_cranes(10) # 申请足够多的船舶
            if idx < len(objs) and objs[idx].get('time'):
                # 验证时间是否延迟了10分钟
                correct_time = time.strftime("%H:%M:%S", time.localtime(time.mktime(time.strptime("8:00:00", "%H:%M:%S")) + 3 * 60 * idx + 10 * 60))
                if objs[idx].get('time') == correct_time:
                    return True
            return False
        except Exception as e:
            print(f"验证第{idx}艘船舶延迟10分钟时发生错误: {e}")
            return False

    def check_duration_extension(self, text):
        """验证: id为X的船舶任务时长延长至20分钟"""
        match = re.search(r"id为(\d+)的船舶", text)
        if not match: return False
        
        target_id = int(match.group(1))
        
        try:
            # init_cranes
            objs = self.module.init_cranes(10)

            target_obj = next((o for o in objs if o.get('id') == target_id), None)
            
            # 验证时长是否为 20 (字符串或数字)
            if target_obj:
                d = target_obj.get('duration')
                return str(d) == "20" or d == 20
            return False
        except:
            return False

    def check_route_fault(self, text):
        """验证: 站位(x,y)...四个点发生故障"""
        # 提取文本中的四个故障点坐标，按出现顺序取前四个
        matches = re.findall(r"\((\d+),(\d+)\)", text)
        if len(matches) < 4:
            return False

        fault_points = [(int(x), int(y)) for x, y in matches[:4]]
        first_fault_point = fault_points[0]

        try:
            # 从(0,0)到第一个故障点，如果不可达(None)表示故障处理正确
            path = self.module.route_planning((0, 0), first_fault_point)
            return path is None
        except:
            return False

    def check_endpoint_change(self, text):
        """验证: 终点调整"""
        # 这个较难验证，通常检查函数运行不报错即可
        # 或者解析出新终点，看路径最后一点是否匹配
        match = re.search(r"调整为\((\d+),(\d+)\)", text)
        if not match: return False
        new_end_x, new_end_y = int(match.group(1)), int(match.group(2))

        try:
            # 传入一个旧终点，看结果是否到了新终点
            path = self.module.route_planning((0,0), (new_end_x-1, new_end_y)) 
            if path and list(path[-1]) == [new_end_x, new_end_y]:
                return True
            return False
        except Exception as e:
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
        details = []

        for event in emergency_list:
            is_solved = False
            
            if "资源不可用" in event:
                is_solved = verifier.check_resource_unavailable(event)
            elif "延迟" in event:
                is_solved = verifier.check_vessel_delay(event)
            elif "四个点发生故障" in event:
                is_solved = verifier.check_route_fault(event)
            elif "时长延长" in event:
                is_solved = verifier.check_duration_extension(event)
            elif "终点" in event:
                is_solved = verifier.check_endpoint_change(event)
            
            if is_solved:
                solved_count += 1
            details.append((event[:10]+"...", "√" if is_solved else "×"))

        return_dict['result'] = {
            'total': len(emergency_list),
            'solved': solved_count,
            'details': details
        }
        
    except Exception as e:
        return_dict['error'] = str(e)

def main(DATASET_FILE,RESULT_DIR):
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

    for i, filename in enumerate(tqdm(files)):
        if i >= len(dataset):
            break
            
        # 获取该文件对应的特情列表 (分号分割)
        situation_str = dataset[i].get("emergency_situation", "")
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
            data = return_dict.get('result', {'total': 0, 'solved': 0})
            res = {'total': data['total'], 'solved': data['solved'], 'status': '正常'}
            if data['solved'] < data['total']:
                print(f"[未完全解决] {filename}: {data['solved']}/{data['total']}")

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

main("datasets/test.json", "MAFIG-cllm/glm-4.7/results")