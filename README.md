## Info
针对某城市餐饮数据集进行数据分析，通过聚类模型获得不同行政区与不同餐饮类型的簇中心，比较距离商店应该在哪方面提升。

## Dependencies
check requirements.txt
## Summary
├─ README.md \
├─ main.py \
├─ dataset/ \
&emsp;└─ food.csv &emsp;//food dataset \
├─ docs/ \
&emsp;└─ 对照表.xlsx \
&emsp;└─ 某市餐饮数据集说明.docx \
├─ map/ &emsp;// map files \
&emsp;└─ food.cpg \
&emsp;└─ food.dbf \
&emsp;└─ food.prj \
&emsp;└─ food.shp \
&emsp;└─ food.shx \
├─ src/ \
&emsp;└─ geopandas_test.ipynb 
## 更改
 - 24.8.19 清理无用文件，加入官方食物数据集和处理好的地图文件
 - 24.8.17 精简dataset dir，增添docs dir存放说明文件
