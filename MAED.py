"""MAED框架"""

import MAED_perception
import MAED_decision
import review_code

if __name__ == "__main__":
    perception_time = MAED_perception.perception_agent("MAED", "/data/huggingface/Qwen2.5-Coder-7B-Instruct")
    decision_time = MAED_decision.decision_agent("MAED", "/data/huggingface/Qwen2.5-Coder-7B-Instruct")
    # review_code.main("datasets/test.json", "MAED/results")
    print(f"感知智能体耗时: {perception_time:.2f}秒")
    print(f"特情决策智能体耗时: {decision_time:.2f}秒")
    print(f"总时间: {perception_time + decision_time:.2f}秒")