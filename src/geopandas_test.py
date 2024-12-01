#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install geopandas')


# In[2]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams["font.sans-serif"] = ["SimHei"]
gdf = gpd.read_file("../map/food.shp")
print(gdf)
gdf["center"] = gdf["geometry"].representative_point()
gdf_points = gdf.copy()
gdf_points.set_geometry("center", inplace = True)
gdf.boundary.plot(cmap='OrRd', figsize=(15, 15))
texts = []

for x, y, label in zip(gdf_points.geometry.x, gdf_points.geometry.y, gdf_points["dt_name"]):
    texts.append(plt.text(x, y, label, fontsize = 12))


# In[3]:


# !pip install ydata-profiling
# !pip install chardet


# In[4]:


import chardet
f1 = open("../dataset/food.csv","rb")
chardet.detect(f1.read())


# In[5]:


from ydata_profiling import ProfileReport
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False # Useless
food_df = pd.read_csv("../dataset/food.csv",encoding="utf-8")
df_report = ProfileReport(food_df)
# // df_report.to_file("../docs/report.html")


# In[6]:


food_df = food_df.replace(0.0, np.nan)
food_df_clean = food_df.copy()
food_df_clean.dropna(how='any',inplace=True)
food_df_clean.drop_duplicates(keep="first",inplace=True) # ? 一大半没了

food_df_clean.to_csv("../dataset/food_preprocessed.csv", encoding="utf-8")

df_report = ProfileReport(food_df_clean)
# // df_report.to_file("../docs/report.html")


# In[7]:


# !pip install pyecharts -U


# In[8]:


from pyecharts.charts import Bar
from pyecharts import options as opts
district_avg = food_df_clean['人均消费'].groupby(food_df_clean['行政区']).mean()
district_avg.plot(kind="bar")
plt.show()
# bar = (
#     Bar()
#     .add_xaxis(district_avg['行政区'].tolist())
#     .add_yaxis("人均消费",district_avg['人均消费'].tolist())
#     .set_global_opts(title_opts=opts.TitleOpts(title="行政区与人均消费间关系"))
# )
# bar.render_notebook()
# ! Key Error
# ? 没有"行政区"键值


# In[9]:


# todo)) gpanda plot绘制


# https://blog.csdn.net/qq_40268672/article/details/109528302

# In[10]:


get_ipython().run_line_magic('pip', 'install altair')


# In[31]:


import altair as alt

click_district = alt.selection_point(fields=["行政区"])

choropleth = ( 
  alt.Chart(
    gdf.drop(columns="center").rename(columns={"dt_id": "行政区", "dt_name": "行政区名称"})
  )
  .mark_geoshape(
    stroke="white",
    strokeWidth=1
  )
  .encode(
    color=alt.Color("人均消费:Q").scale(scheme="reds").legend(orient="left"),
    tooltip=["行政区名称", "人均消费:Q"],
    opacity=alt.condition(click_district, alt.value(1), alt.value(0.2))
  )
  .transform_lookup(
    lookup="行政区",
    from_=alt.LookupData(data=food_df_clean.groupby("行政区")["人均消费"].mean().reset_index(), key="行政区", fields=["人均消费"])
  )
  .properties(
    height=600,
    width=600,
  )
  .add_params(
    click_district
  )
)

bars = (
  alt.Chart(
    food_df_clean.groupby("行政区")["人均消费"].mean().reset_index()
  )
  .mark_bar()
  .encode(
    x="人均消费",
    opacity=alt.condition(click_district, alt.value(1), alt.value(0.2)),
    color=alt.Color("人均消费:Q").scale(scheme="reds"),
    y=alt.Y("行政区").sort("-x"),
    tooltip=["人均消费:Q"]
  )
  .add_params(
    click_district
  )
  .properties(
    width=500
  )
)

text = (
  bars.mark_text(
    align="left",
    baseline="middle",
    dx=3,
    limit=50
  )
  .encode(
    text="人均消费:Q"
  )
  .add_params(
    click_district
  )
)
choropleth | (bars + text)

