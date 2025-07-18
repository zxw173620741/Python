import os
from dotenv import load_dotenv
import requests


load_dotenv()

#ollama函数，提供字符串用户询问词
def ask_ollama(prompt,mod,question):

    api_url = os.getenv("OLLAMA_API_URL")
    renshe="" 
    if mod == 1:    #分析模式
        renshe=os.getenv("OLLAMA_SYSTEM_PROMPT_fenxi")
        print(prompt)
    elif mod == 2:  #预测模式
        renshe=os.getenv("OLLAMA_SYSTEM_PROMPT_yuce")
        print(prompt)
    elif mod == 3:  #提问模式
        renshe=os.getenv("OLLAMA_SYSTEM_PROMPT_tiwen")
    else:           #错误提示@
        print("未检测到MOD")
    payload = {
        "model": os.getenv("OLLAMA_MODEL"),         # 指定模型
        "system": renshe,#系统人设
        # "prompt": os.getenv("OLLAMA_PROMPT"),       # 用户问题
        "prompt":prompt,
        "stream": False,     # 是否流式输出
        "options": {              
            "temperature": 0.7,
            "max_tokens": 20000
        }
    }
    try:
        response = requests.post(
            api_url,
            json=payload,  # 自动序列化为JSON
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError
        return response.json()  # 假设API返回JSON格式的响应
        
    except requests.exceptions.RequestException as e:
        # 处理所有requests可能抛出的异常
        print(f"请求发生错误: {e}")
        return None
    except ValueError as e:
        # 处理JSON解析错误
        print(f"响应JSON解析错误: {e}")
        return None