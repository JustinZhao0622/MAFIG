"""MAFIG框架"""

import logging
import MAFIG_perception
import MAFIG_decision
import review_code

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="MAFIG/MAFIG.log",
    filemode="a+",
)
logger = logging.getLogger(__name__)
MODELS = [
    # {
    #     "name": "Qwen2.5-Coder-7B-Instruct",
    #     "path": "/data/huggingface/Qwen2.5-Coder-7B-Instruct",
    #     "out_dir": "qwen2.5-coder-7b-instruct",
    # },
    # {
    #     "name": "Meta-Llama-3.1-8B-Instruct",
    #     "path": "/data/huggingface/Meta-Llama-3.1-8B-Instruct",
    #     "out_dir": "meta-llama-3.1-8b-instruct",
    # },
    # {
    #     "name": "glm-4-9b-chat",
    #     "path": "/data/huggingface/glm-4-9b-chat",
    #     "out_dir": "glm-4-9b-chat",
    # },
    {
        "name": "Qwen2.5-7B-Instruct",
        "path": "/data/huggingface/Qwen2.5-7B-Instruct",
        "out_dir": "Qwen2.5-7B-Instruct",
    },
    # {
    #     "name": "Qwen3-8B",
    #     "path": "/data/huggingface/Qwen3-8B",
    #     "out_dir": "Qwen3-8B",
    # },
]
if __name__ == "__main__":
    for model in MODELS:
        for run_idx in range(1, 2):
            model_path = model["path"]
            perception_time = MAFIG_perception.perception_agent("MAFIG", model_path)
            decision_time = MAFIG_decision.decision_agent("MAFIG", model_path)
            accuracy = review_code.main("datasets/test.json", "MAFIG/results")
            logger.info(
                f"model={model['name']}, run_idx={run_idx}, perception_time={perception_time:.2f}s, decision_time={decision_time:.2f}s,total_time={perception_time + decision_time:.2f}s, accuracy={accuracy:.4f}"
            )
