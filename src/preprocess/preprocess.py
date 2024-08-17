import pandas as pd
import os 

DATASET_PATH = os.path.join(os.path.abspath(__file__), "..", "..", "..", "dataset")
data = pd.read_csv(os.path.join(DATASET_PATH,"rumor_unofficial.csv"))

# 因为positive_prob和negative_prob重复，丢弃其中一个数据
if "positive_prob" in data:
  data.drop(columns="positive_prob", axis=1, inplace=True)

# 处理情感极性分类
CONFIDENCE_THRESHOLD = 0.2
if "confidence" in data:
  data["sentiment"] -= 1
  data["sentiment"] = [sentiment * confidence if confidence >= CONFIDENCE_THRESHOLD else 0 for (sentiment, confidence) in zip(data['sentiment'], data['confidence']) ]
  data.drop(columns="confidence", axis=1, inplace=True)

data.to_csv(os.path.join(DATASET_PATH,"rumor_preprocessed.csv"))