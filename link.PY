from email import header
import os
import mysql.connector
import json
import requests
from dotenv import load_dotenv

load_dotenv()

#请求数据库
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE'),
        port=int(os.getenv('MYSQL_PORT'))
    )

# 
try:
    conn=get_db_connection()
    print("连接成功")
except mysql.connector.Error as err:
    # 发生异常时执行的代码
    print("连接失败")

cursor = conn.cursor()

cursor.execute("select * from ads_fps")

data = cursor.fetchall()


#ollama函数
def ask_ollama():
    api_url = os.getenv("OLLAMA_API_URL")
    payload = {
        "model": os.getenv("OLLAMA_MODEL"),         # 指定模型
        "system": os.getenv("OLLAMA_SYSTEM_PROMPT"),#系统人设
        "prompt": os.getenv("OLLAMA_PROMPT"),       # 用户问题
        "stream": False,     # 是否流式输出
        "options": {              
            "temperature": 0.7,
            "max_tokens": 5000
        }
    }
    response = requests.post(
            api_url,
            json=payload,  # 自动序列化为JSON
            headers={"Content-Type": "application/json"},
    )
    return response

print(ask_ollama().text)

