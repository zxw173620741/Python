from email import header
from http.client import PRECONDITION_FAILED
from logging import info
import os
import mysql.connector
import json
import requests
from dotenv import load_dotenv
from flask import Flask, Response, request, jsonify

app = Flask(__name__)
#读取配置文件
load_dotenv()





#ollama函数，提供字符串用户询问词
def ask_ollama(prompt):
    api_url = os.getenv("OLLAMA_API_URL")
    payload = {
        "model": os.getenv("OLLAMA_MODEL"),         # 指定模型
        "system": os.getenv("OLLAMA_SYSTEM_PROMPT"),#系统人设
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
    

#数据分类阶段,生产问题的三个问题
def shengchan(data):
    categories = {
        "原因一：产能利用率不足": {"brands": [], "metrics": []},
        "原因二：库存周转率低下": {"brands": [], "metrics": []},
        "原因三：生产质量不稳定": {"brands": [], "metrics": []},
    }
    for brand in data:
        if brand.get("avg_utilization")<85 and brand.get("completion_rate")<90 and brand.get("avg_efficiency"):
            categories["原因一：产能利用率不足"]["brands"].append(brand.get("brand"))
            categories["原因一：产能利用率不足"]["metrics"].append({
                "brand": brand.get("brand"),
                "avg_utilization": brand.get("avg_utilization"),
                "completion_rate": brand.get("completion_rate"),
                "avg_efficiency": brand.get("avg_efficiency"),
            })
        if brand.get("inventory_turnover_rate")<25 and brand.get("avg_inventory_level")>1000:
            categories["原因二：库存周转率低下"]["brands"].append(brand.get("brand"))
            categories["原因二：库存周转率低下"]["metrics"].append({
                "brand": brand.get("brand"),
                "inventory_turnover_rate": brand.get("inventory_turnover_rate"),
                "avg_inventory_level": brand.get("avg_inventory_level"),
            })
        if brand.get("qualified_rate")<98 and brand.get("defect_rate")>=1.5:
            categories["原因三：生产质量不稳定"]["brands"].append(brand.get("brand"))
            categories["原因三：生产质量不稳定"]["metrics"].append({
                "brand": brand.get("brand"),
                "qualified_rate": brand.get("qualified_rate"),
                "defect_rate": brand.get("defect_rate"),
            })
    return categories

#制作用户请求语句,提供字典
def call_llm_massage(data):
    prompt = "根据生产监控系统分类结果，请进行业务影响分析和改进的报告：\n\n"
    prompt = f"作为生产专家，请针对以下问题给出每个品牌一到两个主要原因，其他的原因可以一笔带过，主要解决核心问题并给出精准的解决方案，需要精确到领导可以直接下发方案的提议\n"
    for i,j in data.items():
        prompt += f"问题类型: {i}\n"
        for metric in j["metrics"]:
            brand = metric.get("brand", "未知品牌")
            # 拼接该品牌所有指标的key和value
            metric_str = ', '.join(f"{k}: {v}" for k, v in metric.items() if k != "brand")
            prompt += f"- 品牌: {brand}，指标: {metric_str}\n"
    return prompt


@app.route('/data', methods=['POST'])
def getdata():
    data = request.get_json()
    data = shengchan(data)
    data = call_llm_massage(data)
    data = ask_ollama(data)
    # 假设 data 是 dict，里面有字符串字段包含中文
    ok_data = {
    "response": data.get("response")
    }
    json_str = json.dumps(ok_data, ensure_ascii=False)  # 这里关闭 ASCII 转义
    return Response(json_str, content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True)