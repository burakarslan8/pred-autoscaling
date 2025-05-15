import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("augmented_binary_for_classification.csv", parse_dates=["Timestamp"])
df = df.sort_values("Timestamp").dropna().reset_index(drop=True)

feature_cols = [
    "cpu_usage_idle", "cpu_usage_idle_lag1", "cpu_usage_idle_lag2", "cpu_usage_idle_lag3",
    "cpu_idle_mean5", "cpu_idle_std5",
    "mem_used_percent", "mem_used_percent_lag1", "mem_used_percent_lag2", "mem_used_percent_lag3",
    "mem_used_mean5", "mem_used_std5",
    "cpu_mem_ratio", "cpu_usage_iowait", "swap_used_percent", "diskio_io_time",
    "hour", "weekday"
]
X = df[feature_cols]
y = df["is_scale_up"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

MODEL_PATH = "xgb_scale_up_classifier.pkl"

def train_and_save_model(X_train, y_train):
    model = XGBClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss"
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print("Model trained and saved.")
    return model

def load_or_train_model(X_train, y_train):
    if os.path.exists(MODEL_PATH):
        print("Loading existing model...")
        return joblib.load(MODEL_PATH)
    else:
        print("No model found. Training new model...")
        return train_and_save_model(X_train, y_train)

model = load_or_train_model(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

print(f"Accuracy: {acc:.4f}")
print(f"ROC AUC: {roc_auc:.4f}\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, digits=3, target_names=["Not Scale Up", "Scale Up"]))

conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Not Up", "Up"], yticklabels=["Not Up", "Up"])
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()
