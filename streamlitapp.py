import streamlit as st
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import altair as alt
import json

with open("./data.json", encoding="utf-8", mode="r") as f:
  cluster_data = json.load(f)

food_df_clean = pd.read_csv("./dataset/food_preprocessed.csv")
gdf = gpd.read_file("./map/food.shp")
# st.set_page_config(layout="wide")
dt = st.selectbox("选择一个行政区", gdf["dt_name"].unique())
classification = st.selectbox("选择一个餐饮类别", food_df_clean["类别"].unique())
count = st.number_input("点评数", 0, None, 0)
flavor = st.number_input("口味评分", 0.0, 10.0, 6.0, 0.01)
env = st.number_input("环境评分", 0.0, 10.0, 6.0, 0.01)
service = st.number_input("服务评分", 0.0, 10.0, 6.0, 0.01)
earning = st.number_input("人均消费", 0.0)



def render_score_distribution(df, field, target):
  bar_data = df.value_counts(field).reset_index()
  color = alt.condition(
                        alt.datum[field] == target,
                        alt.value('red'), 
                        alt.value('skyblue')
                    )
  bar_chart = (
    alt.Chart(bar_data)
    .mark_bar(
      width=10
    )
    .encode(
      x=field,
      y=alt.Y("count", title="数量"),
      color=color
    )
  )
  with st.container():
    st.markdown(f"### {field}评分分布")
    st.altair_chart(bar_chart, use_container_width=True)

def find_nearest_data(df, flavor, env, service):
  # 计算每个数据点与目标值的距离
  df['distance'] = abs(df['口味'] - flavor) + abs(df['环境'] - env) + abs(df['服务'] - service)
  # 找到距离最小的前三个数据点
  nearest_data = df.nsmallest(5, 'distance')
  return nearest_data


if dt or classification or count or flavor or env or service:
  # if st.button("确认"):
  dt_id = gdf[gdf["dt_name"] == dt]["dt_id"].iloc[0]
  df = food_df_clean[food_df_clean["行政区"] == dt_id]
  df = df[df["类别"] == classification]
  new_row = pd.Series({"点评数": count, "口味": flavor, "环境": env, "服务": service})
  df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
  render_score_distribution(df, "口味", flavor)
  render_score_distribution(df, "环境", env)
  render_score_distribution(df, "服务", service)
  nearest_data = find_nearest_data(df[:-1], flavor, env, service)
  with st.container():
    st.markdown(f"### 竞争对手")
    st.dataframe(nearest_data.reset_index()[["类别", "行政区", "点评数", "口味", "环境", "服务", "人均消费"]], use_container_width=True)

  clusters = cluster_data[f"{dt_id},{classification}"]
  best_cluster = clusters[-1]
  distances = []
  s = 0
  for i, value in enumerate(best_cluster):
    field = ["口味","环境","服务"][i]
    distance = (value - [flavor, env, service][i]) ** 2
    if distance > 0:
      distances.append([field, distance])
      s += distance
  for i, (field, distance) in enumerate(distances):
    distances[i][1] = round(distance / s, 3)
  if len(distances) > 0:
    with st.container():
      st.markdown(f"### 需要改进的评分")
      data = pd.DataFrame({"field": list(map(lambda x: x[0], distances)), "distance": list(map(lambda x: x[1], distances))})
      base = alt.Chart(data).encode(
        alt.Theta("distance:Q").stack(True),
        alt.Radius("distance").scale(zero=True, rangeMin=20),
        color=alt.Color("distance:N", title="比例"),
      )
      c1 = base.mark_arc(innerRadius=20)
      c2 = base.mark_text(radiusOffset=20).encode(text="field")
      st.altair_chart((c1 + c2), use_container_width=True)
  # median_data = df[["口味", "环境", "服务", "人均消费"]].median().reset_index(drop=True)
  # my_data = pd.Series([flavor, env, service, earning])
  # data = pd.concat([my_data, median_data], axis=1)
  # data.rename(columns={0: "我的", 1: "中位数据"}, inplace=True)
  # data.index = pd.Index(["口味", "环境", "服务", "人均消费"])
  # data.reset_index(inplace=True)
  # st.write(data)
  # plot_radar_chart(data)



