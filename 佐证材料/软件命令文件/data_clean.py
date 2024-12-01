import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import chardet
f1 = open("../dataset/food.csv","rb")
chardet.detect(f1.read())

from ydata_profiling import ProfileReport
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # Useless
food_df = pd.read_csv("../dataset/food.csv",encoding="utf-8")
df_report = ProfileReport(food_df)
# // df_report.to_file("../docs/report.html")
food_df = food_df.replace(0.0, np.nan)
food_df_clean = food_df.copy()
food_df_clean.dropna(how='any',inplace=True)
food_df_clean.drop_duplicates(keep="first",inplace=True) # ? 一大半没了

food_df_clean.to_csv("../dataset/food_preprocessed.csv", encoding="utf-8")

df_report = ProfileReport(food_df_clean)
# // df_report.to_file("../docs/report.html")