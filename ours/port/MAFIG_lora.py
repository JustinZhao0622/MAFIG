"""
MAFIG_lora框架
包含llama factory微调和模型合并
存储在/root/code/neuralcomputing-models/gangkou
"""

import os
import time
import shutil
import subprocess
import logging
import json
import torch
import gc
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer,AutoModelForCausalLM
from peft import PeftModel
import prompts as prompts_mod
import MAFIG_decision

import review_code
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='MAFIG_lora.log',
                    filemode='a'
                    )
logger = logging.getLogger(__name__)

scenario = "gangkou"
raw_model_path = "/data/huggingface/Qwen2.5-Coder-7B-Instruct"
perception_models_path = f"/root/code/neuralcomputing-models/{scenario}/perception"
perception_combined_models_path = f"/root/code/neuralcomputing-models/{scenario}/combined_perception"
decision_models_path = f"/root/code/neuralcomputing-models/{scenario}/decision"
decision_combined_models_path = f"/root/code/neuralcomputing-models/{scenario}/combined_decision"
DIR = "/root/code/MAFIG/ours/port/MAFIG_lora/"
DATASET_FILE = "datasets/test.json"
def lora_perception_agent():
    """
    微调并合并感知智能体
    """
    with open("perception_train_datas.json", "r", encoding="utf-8") as f:
        perception_train_datas = json.load(f)[:30]
    with open("datasets/perception_train_datas.json", "w", encoding="utf-8") as f:
        json.dump(perception_train_datas, f, ensure_ascii=False, indent=4)
        
    learning_rate = 5e-5
    num_train_epochs = 3
    per_device_train_batch_size = 2
    gradient_accumulation_steps = 2
    
    if os.path.exists(perception_models_path):
        shutil.rmtree(perception_models_path)
    os.makedirs(perception_models_path)
    
    if os.path.exists(perception_combined_models_path):
        shutil.rmtree(perception_combined_models_path)
    os.makedirs(perception_combined_models_path)
    
    train_args = [
        "--stage", "sft",
        "--do_train", "True",
        "--model_name_or_path", raw_model_path,
        "--preprocessing_num_workers", "16",
        "--finetuning_type", "lora",
        "--template", "qwen",
        "--flash_attn", "auto",
        "--dataset_dir", "/root/code/MAFIG/ours/port/datasets",
        "--dataset", "Perception_Train_data",
        "--cutoff_len", "2048",
        "--learning_rate", str(learning_rate),
        "--num_train_epochs", str(num_train_epochs),
        "--max_samples", "100000",
        "--per_device_train_batch_size", str(per_device_train_batch_size),
        "--gradient_accumulation_steps", str(gradient_accumulation_steps),
        "--lr_scheduler_type", "cosine",
        "--max_grad_norm", "1.0",
        "--logging_steps", "5",
        "--save_steps", "100",
        "--warmup_steps", "0",
        "--packing", "False",
        "--report_to", "none",
        "--output_dir", perception_models_path,
        "--bf16", "True",
        "--plot_loss", "True",
        "--trust_remote_code", "True",
        "--ddp_timeout", "180000000",
        "--include_num_input_tokens_seen", "True",
        "--optim", "adamw_torch",
        "--lora_rank", "8",
        "--lora_alpha", "16",
        "--lora_dropout", "0",
        "--lora_target", "all",
    ]
    subprocess.run(
        ["conda", "run", "-n", "llama_new", "--no-capture-output",
         "llamafactory-cli", "train"] + train_args,
        check=True, env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"},
    )
    # 合并模型
    base_model = AutoModelForCausalLM.from_pretrained(raw_model_path, torch_dtype="auto",trust_remote_code=True)
    base_tokenizer = AutoTokenizer.from_pretrained(raw_model_path, trust_remote_code=True)
    lora_model = PeftModel.from_pretrained(base_model, perception_models_path)
    combined_model = lora_model.merge_and_unload()
    combined_model.save_pretrained(perception_combined_models_path)
    base_tokenizer.save_pretrained(perception_combined_models_path)
def perception_agent():
    """
    测试感知智能体
    """
    time_start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(perception_combined_models_path, trust_remote_code=True)
    llm = LLM(
        model=perception_combined_models_path,
        device="cuda",
        dtype="auto",
        trust_remote_code=True,
        gpu_memory_utilization=0.9,
    )
    sampling_params = SamplingParams(temperature=0, top_p=0.95, max_tokens=2560)
    inputs = []
    with open(f"datasets/test.json", "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)
    for idx, emergency_situation in enumerate(emergency_situations):
        messages = [
            {"role": "system", "content": prompts_mod.perception_system_prompt},
            {"role": "user", "content": prompts_mod.perception_user_prompt.format(EMERGENCY_SITUATIONS=emergency_situation["emergency_situation"], 
                                                        nums=len(emergency_situation["emergency_situation"].split(";")))}
        ]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs.append(text)
    outputs = llm.generate(inputs, sampling_params)
    correct = 0
    for i, output in enumerate(outputs):
        text = eval(output.outputs[0].text.replace("```python", "").replace("```", "").strip())
        if text == emergency_situations[i]["functions"]:
            correct += 1
    print(f"准确率: {correct}/{len(outputs)} ({correct/len(outputs)*100:.1f}%)")
    print(f"感知智能体耗时: {time.time() - time_start:.2f}秒")
def decision_loss_agent():
    """
    向模型的tokenizer添加<<EDIT_START>>和<<EDIT_END>>，并初始化对应embedding
    """
    model_path = raw_model_path
    save_path = raw_model_path + "-edit"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True) 
    tokenizer.add_special_tokens({"additional_special_tokens": ["<<EDIT_START>>", "<<EDIT_END>>"]}) 
    # 保存 tokenizer 到新目录 
    tokenizer.save_pretrained(save_path) 
    # 同时把原模型的 config 等文件复制/保存（最简单做法：把模型也保存到 out_path） 
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True) # 
    # 关键：扩展 embedding 以容纳新 token 
    model.resize_token_embeddings(len(tokenizer)) # 
    # 保存模型到新目录 
    model.save_pretrained(save_path)
    model_path=raw_model_path + "-edit"
    save_path = raw_model_path + "-edit-init" 
    
    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)
    print(f"正在加载模型: {model_path} ...")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True, torch_dtype="auto")

    # 2. 获取 Embedding 权重
    embedding_matrix = model.get_input_embeddings().weight.data
    vocab_size, hidden_dim = embedding_matrix.shape

    # 3. 找到新 Token 的 ID
    new_tokens = ["<<EDIT_START>>", "<<EDIT_END>>"]
    new_ids = tokenizer.convert_tokens_to_ids(new_tokens)
    print(f"新 Token IDs: {new_ids}")

    # 4. 计算旧 Token 的均值和方差 (用来初始化新 Token)
    # 我们只用前 151665 个原有词来计算，避开新加的
    old_embeddings = embedding_matrix[:new_ids[0]] 
    mean_emb = old_embeddings.mean(dim=0)
    std_emb = old_embeddings.std(dim=0)

    # 5. 核心修复：给新 Token 赋值
    print("正在执行均值初始化...")
    for idx in new_ids:
        # 赋值为：均值 + 微小的随机扰动
        # 这样既符合整体分布，又保留了一点点随机性方便梯度下降
        embedding_matrix[idx] = mean_emb + torch.randn_like(mean_emb) * std_emb * 0.01

    # 6. 如果模型共享输出权重 (Tie Weights)，通常会自动更新，但为了保险再检查一下
    output_embeddings = model.get_output_embeddings()
    if output_embeddings is not None and output_embeddings.weight.data_ptr() != embedding_matrix.data_ptr():
        print("同步更新 Output Embeddings...")
        output_embeddings.weight.data[new_ids] = embedding_matrix[new_ids]

    # 7. 保存修复后的模型
    print(f"保存初始化后的模型到: {save_path}")
    model.save_pretrained(save_path)
    tokenizer.save_pretrained(save_path)
    print("完成！请使用新路径进行微调。")  
def lora_decision_agent():
    """
    微调并合并决策智能体（基于添加了EDIT tokens的模型）
    """
    edit_model_path = raw_model_path + "-edit-init"
    # edit_model_path = raw_model_path
    
    learning_rate = 5e-5
    num_train_epochs = 3
    per_device_train_batch_size = 2
    gradient_accumulation_steps = 2

    if os.path.exists(decision_models_path):
        shutil.rmtree(decision_models_path)
    os.makedirs(decision_models_path)

    if os.path.exists(decision_combined_models_path):
        shutil.rmtree(decision_combined_models_path)
    os.makedirs(decision_combined_models_path)

    train_args = [
        "--stage", "sft",
        "--do_train", "True",
        "--model_name_or_path", edit_model_path,
        "--preprocessing_num_workers", "16",
        "--finetuning_type", "lora",
        "--template", "qwen",
        "--flash_attn", "auto",
        "--dataset_dir", "/root/code/MAFIG/ours/port/datasets",
        "--dataset", "Decision_Train_data",
        "--cutoff_len", "2048",
        "--learning_rate", str(learning_rate),
        "--num_train_epochs", str(num_train_epochs),
        "--max_samples", "100000",
        "--per_device_train_batch_size", str(per_device_train_batch_size),
        "--gradient_accumulation_steps", str(gradient_accumulation_steps),
        "--lr_scheduler_type", "cosine",
        "--max_grad_norm", "1.0",
        "--logging_steps", "5",
        "--save_steps", "100",
        "--warmup_steps", "0",
        "--packing", "False",
        "--report_to", "none",
        "--output_dir", decision_models_path,
        "--bf16", "True",
        "--plot_loss", "True",
        "--trust_remote_code", "True",
        "--ddp_timeout", "180000000",
        "--include_num_input_tokens_seen", "True",
        "--optim", "adamw_torch",
        "--lora_rank", "8",
        "--lora_alpha", "16",
        "--lora_dropout", "0",
        "--lora_target", "all",
    ]
    time_start = time.time()
    subprocess.run(
        ["conda", "run", "-n", "llama_new", "--no-capture-output",
         "llamafactory-cli", "train"] + train_args,
        check=True, env={**os.environ, "CUDA_VISIBLE_DEVICES": "0"},
    )
    time_end = time.time()
    # 合并模型
    base_model = AutoModelForCausalLM.from_pretrained(edit_model_path, torch_dtype="auto", trust_remote_code=True)
    base_tokenizer = AutoTokenizer.from_pretrained(edit_model_path, trust_remote_code=True)
    lora_model = PeftModel.from_pretrained(base_model, decision_models_path)
    combined_model = lora_model.merge_and_unload()
    combined_model.save_pretrained(decision_combined_models_path)
    base_tokenizer.save_pretrained(decision_combined_models_path)
    # 【新增】显式销毁对象并清空缓存
    del lora_model
    del base_model
    del combined_model
    gc.collect()
    torch.cuda.empty_cache() # 清空 PyTorch 缓存占用的显存
    return time_end - time_start
def decision_agent():
    """
    测试决策智能体：用合并后的决策模型处理
    """
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        emergency_situations = json.load(f)
    for emergency_situation in emergency_situations:
        emergency_situation["perception_functions"] = emergency_situation["functions"]
    with open(f"{DIR}/perception_events.json", "w+", encoding="utf-8") as f:
        json.dump(emergency_situations, f, ensure_ascii=False, indent=4)
    return MAFIG_decision.decision_agent(DIR, decision_combined_models_path)

if __name__ == "__main__":
    # 感知智能体
    # lora_perception_agent()
    # perception_agent()
    # 决策智能体loss调整
    # decision_loss_agent()
    nums = [60,70,80,100]
    for num in nums:
        with open("/root/code/MAFIG/ours/port/decision_loss_train_datas.json","r", encoding="utf-8") as f:
            decision_loss_train_datas = json.load(f)[:num]
        with open("/root/code/MAFIG/ours/port/datasets/decision_loss_train_datas.json","w", encoding="utf-8") as f:
            json.dump(decision_loss_train_datas, f, ensure_ascii=False, indent=4)
        # 决策智能体
        time_lora = lora_decision_agent()
        time_decision = decision_agent()
        gc.collect()
        torch.cuda.empty_cache()
        accuracy = review_code.main(DATASET_FILE, DIR + "results")
        logger.info(f"num: {num}, accuracy: {accuracy}, time_lora: {time_lora}, time_decision: {time_decision}")