"""MAED框架"""
import logging
import MAED_perception
import MAED_decision
import review_code

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='MAED.log',
                    filemode='a'
                    )
logger = logging.getLogger(__name__)
MODELS = [
    {
        "name": "Qwen2.5-Coder-7B-Instruct",
        "path": "/data/huggingface/Qwen2.5-Coder-7B-Instruct",
    },
    {
        "name": "Meta-Llama-3.1-8B-Instruct",
        "path": "/data/huggingface/Meta-Llama-3.1-8B-Instruct",
    },
    {
        "name": "glm-4-9b-chat",
        "path": "/data/huggingface/glm-4-9b-chat",
    }
]
if __name__ == "__main__":
    # Qwen2.5-Coder-7B-Instruct  Meta-Llama-3.1-8B-Instruct  glm-4-9b-chat
    for model in MODELS:
        for run_idx in range(1, 3):
            model_path = model["path"]
            perception_time = MAED_perception.perception_agent("MAED", model_path)
            decision_time = MAED_decision.decision_agent("MAED", model_path)
            accuracy = review_code.main("datasets/test.json", "MAED/results")
            logger.info(f"model={model['name']}, run_idx={run_idx}, perception_time={perception_time:.2f}s, decision_time={decision_time:.2f}s, accuracy={accuracy:.4f}")