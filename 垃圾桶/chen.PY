import requests

# Ollama配置
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "deepseek-r1:7b",
    "temperature": 0.7
}


def extract_brand_metrics(input_data):
    result = []
    if not isinstance(input_data, list):
        input_data = [input_data]
    for brand_data in input_data:
        try:
            extracted_data = {
                "brand": brand_data.get("brand"),
                "avg_utilization": brand_data.get("avg_utilization"),
                "completion_rate": brand_data.get("completion_rate"),
                "avg_efficiency": brand_data.get("avg_efficiency"),
                "inventory_turnover_rate": brand_data.get("inventory_turnover_rate"),
                "avg_inventory_level": brand_data.get("avg_inventory_level"),
                "qualified_rate": brand_data.get("qualified_rate"),
                "defect_rate": brand_data.get("defect_rate"),
                "plan_completion_rate": brand_data.get("plan_completion_rate")
            }
            result.append(extracted_data)
        except AttributeError:
            continue
    return result


def classify_brands(extracted_data):
    categories = {
        "原因一：设备利用率低下": {"brands": [], "metrics": []},
        "原因二：生产计划与实际脱节": {"brands": [], "metrics": []},
        "原因三：质量缺陷拉低有效产出": {"brands": [], "metrics": []},
        "原因四：库存积压占用资源": {"brands": [], "metrics": []}
    }
    classified_brands = set()

    for brand in extracted_data:
        brand_name = brand["brand"]
        if brand_name in classified_brands:
            continue

        if brand.get("avg_utilization", 0) < 75 and brand.get("inventory_turnover_rate", 0) < 30:
            categories["原因一：设备利用率低下"]["brands"].append(brand_name)
            categories["原因一：设备利用率低下"]["metrics"].append({
                "brand": brand_name,
                "avg_utilization": brand.get("avg_utilization"),
                "inventory_turnover_rate": brand.get("inventory_turnover_rate")
            })
            classified_brands.add(brand_name)
            continue

        if brand.get("plan_completion_rate", 100) < 80 and brand.get("completion_rate", 100) < 90:
            categories["原因二：生产计划与实际脱节"]["brands"].append(brand_name)
            categories["原因二：生产计划与实际脱节"]["metrics"].append({
                "brand": brand_name,
                "plan_completion_rate": brand.get("plan_completion_rate"),
                "completion_rate": brand.get("completion_rate")
            })
            classified_brands.add(brand_name)
            continue

        if brand.get("defect_rate", 0) > 2:
            categories["原因三：质量缺陷拉低有效产出"]["brands"].append(brand_name)
            categories["原因三：质量缺陷拉低有效产出"]["metrics"].append({
                "brand": brand_name,
                "defect_rate": brand.get("defect_rate")
            })
            classified_brands.add(brand_name)
            continue

        if brand.get("avg_inventory_level", 0) > 1000:
            categories["原因四：库存积压占用资源"]["brands"].append(brand_name)
            categories["原因四：库存积压占用资源"]["metrics"].append({
                "brand": brand_name,
                "avg_inventory_level": brand.get("avg_inventory_level")
            })
            classified_brands.add(brand_name)
    return categories


def generate_analysis_prompt(classified_data):
    prompt = "根据生产监控系统分类结果，请进行业务影响分析和改进建议：\n\n"
    for category, data in classified_data.items():
        prompt += f"【{category}】\n"
        prompt += f"涉及品牌：{', '.join(data['brands']) if data['brands'] else '无'}\n"
        if data["metrics"]:
            prompt += "关键指标：\n"
            for metric in data["metrics"]:
                brand = metric["brand"]
                if "avg_utilization" in metric:
                    prompt += f"- {brand}: 设备利用率{metric['avg_utilization']}%, 库存周转率{metric['inventory_turnover_rate']}\n"
                elif "plan_completion_rate" in metric:
                    prompt += f"- {brand}: 计划完成率{metric['plan_completion_rate']}%, 实际完成率{metric['completion_rate']}%\n"
                elif "defect_rate" in metric:
                    prompt += f"- {brand}: 缺陷率{metric['defect_rate']}%\n"
                elif "avg_inventory_level" in metric:
                    prompt += f"- {brand}: 库存量{metric['avg_inventory_level']}件\n"
        prompt += "\n"
    prompt += "请按照以下格式分析：\n1. 问题本质分析\n2. 潜在业务影响\n3. 改进建议\n4. 预期效果\n"
    return prompt


def call_local_llm(prompt):
    try:
        response = requests.post(
            f"{OLLAMA_CONFIG['base_url']}/api/generate",
            json={
                "model": OLLAMA_CONFIG['model'],
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": OLLAMA_CONFIG['temperature']}
            }
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"模型调用失败：{str(e)}"


# 示例输入数据
input_data = [
    {
        "actual_volume": 66,
        "avg_efficiency": 96.6,
        "avg_inventory_level": 66,
        "avg_utilization": 60,
        "brand": "XW品牌",
        "completion_rate": 66,
        "defect_rate": 5,
        "inventory_turnover_rate": 25,
        "plan_completion_rate": 99,
        "qualified_rate": 100,
        "statistic_date": "2025-07-30 23:22:30",
        "target_volume": 66
    },
    {
        "actual_volume": 76,
        "avg_efficiency": 96.6,
        "avg_inventory_level": 66,
        "avg_utilization": 60,
        "brand": "CY品牌",
        "completion_rate": 66,
        "defect_rate": 5,
        "inventory_turnover_rate": 75,
        "plan_completion_rate": 89,
        "qualified_rate": 100,
        "statistic_date": "2025-07-30 23:22:30",
        "target_volume": 86
    },
    {
        "actual_volume": 120,
        "avg_efficiency": 85.0,
        "avg_inventory_level": 1200,
        "avg_utilization": 70,
        "brand": "HighInventory品牌",
        "completion_rate": 85,
        "defect_rate": 1,
        "inventory_turnover_rate": 20,
        "plan_completion_rate": 75,
        "qualified_rate": 99,
        "statistic_date": "2025-07-30 23:22:30",
        "target_volume": 150
    },
    {
        "actual_volume": 90,
        "avg_efficiency": 90.0,
        "avg_inventory_level": 800,
        "avg_utilization": 50,
        "brand": "Defective品牌",
        "completion_rate": 88,
        "defect_rate": 3,
        "inventory_turnover_rate": 15,
        "plan_completion_rate": 95,
        "qualified_rate": 97,
        "statistic_date": "2025-07-30 23:22:30",
        "target_volume": 100
    },
    {
        "actual_volume": 90,
        "avg_efficiency": 90.0,
        "avg_inventory_level": 800,
        "avg_utilization": 50,
        "brand": "Defective品牌",
        "completion_rate": 88,
        "defect_rate": 3,
        "inventory_turnover_rate": 15,
        "plan_completion_rate": 95,
        "qualified_rate": 97,
        "statistic_date": "2025-08-30 23:22:30",
        "target_volume": 100
    }
]

if __name__ == '__main__':
    # 处理流程
    extracted_metrics = extract_brand_metrics(input_data)
    classified_brands = classify_brands(extracted_metrics)

    # 打印提示词
    analysis_prompt = generate_analysis_prompt(classified_brands)
    print("\n发送给大模型的提示词：")
    print(analysis_prompt[:500] + "...")  # 打印前500字符示例

    # 调用模型并打印结果
    analysis_result = call_local_llm(analysis_prompt)
    print("\n大模型分析结果：")
    print("=" * 80)
    print(analysis_result)
    print("=" * 80)