from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import pandas as pd
import os

DATASET_PATH = os.path.join(__file__, "..", "..", "..", "dataset", "rumor_preprocessed.csv")

data = pd.read_csv(DATASET_PATH)

features = data.drop(columns="abnormal")
target = data["abnormal"]

# 标准化
scalar = StandardScaler()
scalar.fit(features)
features = scalar.transform(features)

# 分割数据集
x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=1337)

# 建立模型并训练
classifier = MLPClassifier(activation="tanh", solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(100,), random_state=1337)
classifier.fit(x_train, y_train)

# 评估结果
y_pred = classifier.predict(x_test)
print(f"{'Loss':<10} {classifier.loss_}")
print(f"{'Acc':<10} {accuracy_score(y_test, y_pred)}") 
print(f"{'Precision':<10} {precision_score(y_test, y_pred)}")
print(f"{'Recall':<10} {recall_score(y_test, y_pred)}")
print(f"{'F1 score':<10} {f1_score(y_test, y_pred)}")