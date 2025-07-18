#数据分类阶段,生产问题的三个问题
def shengchan_data(data):
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
def shengchan_prompt(data):
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