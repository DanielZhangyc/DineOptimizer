import pandas as pd

# 读取数据集
food_df_clean = pd.read_csv("../dataset/food_preprocessed.csv")

# 选择部分数据（例如前10行）
sample_data = food_df_clean.head(10)

# 指定需要打印的列
columns_to_include = ["行政区", "类别", "口味", "服务", "环境", "人均消费"]

# 生成 LaTeX 表格代码
latex_table = sample_data[columns_to_include].to_latex(index=False, escape=False, caption="餐饮数据示例", label="tab:sample_data")

# 保存为 .tex 文件
with open("sample_data_table.tex", "w", encoding="utf-8") as f:
    f.write(latex_table)

print("LaTeX 表格代码已生成并保存为 sample_data_table.tex 文件。")