import pandas as pd

INPUT_PATH = "augmented_binary_for_classification_1month.csv"
OUTPUT_PATH = "augmented_binary_for_classification_1month_fe.csv"

df = pd.read_csv(INPUT_PATH, parse_dates=["Timestamp"])

df = df.sort_values('Timestamp')

df['cpu_idle_delta'] = df['cpu_usage_idle'].diff().fillna(0)
df['mem_used_delta'] = df['mem_used_percent'].diff().fillna(0)

df['cpu_idle_drop_flag'] = (df['cpu_idle_delta'] < -10).astype(int)

df['mem_used_spike_flag'] = (df['mem_used_delta'] > 10).astype(int)

df['cpu_usage_idle_lag1'] = df['cpu_usage_idle'].shift(1)
df['cpu_usage_idle_lag2'] = df['cpu_usage_idle'].shift(2)
df['cpu_usage_idle_lag3'] = df['cpu_usage_idle'].shift(3)
df['cpu_idle_mean5'] = df['cpu_usage_idle'].rolling(window=5).mean()
df['cpu_idle_std5'] = df['cpu_usage_idle'].rolling(window=5).std()
df['mem_used_percent_lag1'] = df['mem_used_percent'].shift(1)
df['mem_used_percent_lag2'] = df['mem_used_percent'].shift(2)
df['mem_used_percent_lag3'] = df['mem_used_percent'].shift(3)
df['mem_used_mean5'] = df['mem_used_percent'].rolling(window=5).mean()
df['mem_used_std5'] = df['mem_used_percent'].rolling(window=5).std()
df['cpu_mem_ratio'] = df['cpu_usage_idle'] / (df['mem_used_percent'] + 1e-5)

df.to_csv(OUTPUT_PATH, index=False)
print(f"Feature engineered dataset saved as {OUTPUT_PATH}")
