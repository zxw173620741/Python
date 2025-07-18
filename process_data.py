
import json
from shengchan import *
from split_body_flask import split_body
from ollama import *

#数据加工过程
def process_data(input_data):
    data,mod,question = split_body(input_data)
    data = shengchan_data(data)
    if mod ==3:
        chuli_data=input_data.get("data")
        string_data = json.dumps(input_data, ensure_ascii=False)
        return ask_ollama(string_data,mod,question)['response']
    elif mod==2:
        string_data=json.dumps(data, ensure_ascii=False)
        return ask_ollama(string_data,mod,question)['response']
    else:
        prompt = shengchan_prompt(data)
        return ask_ollama(prompt,mod,question)['response']
    
