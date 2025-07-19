
import json
from shengchan import *
from split_body_flask import split_body
from ollama import *

#数据加工过程
def process_data(input_data):
    data,mod,question = split_body(input_data)
    shengchan_shujv = shengchan_data(data)
    if mod ==3:
        chuli_data=input_data.get("data")
        string_data = json.dumps(input_data, ensure_ascii=False)
        return ask_ollama(string_data,mod,question)['response']
    elif mod==2:
        string_data = json.dumps(data, ensure_ascii=False)
        return ask_ollama(string_data,mod,None)['response']
    else:
        prompt = shengchan_prompt(shengchan_shujv)
        return ask_ollama(prompt,mod,None)['response']
    
def process_data_liushi(input_data):
    """统一改为流式输出"""
    data, mod, question = split_body(input_data)
    
    try:
        # 构造prompt（所有分支统一处理）
        if mod == 3:
            prompt = json.dumps(input_data, ensure_ascii=False)
        elif mod == 2:
            prompt = json.dumps(data, ensure_ascii=False)
        else:
            shengchan_shujv = shengchan_data(data)
            prompt = shengchan_prompt(shengchan_shujv)

        # 统一调用流式ask_ollama
        for chunk in ask_ollama_liushi(prompt, mod, question):
            yield chunk

    except Exception as e:
        yield f"[处理错误] {str(e)}"
