import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("augmented_binary_for_classification.csv", parse_dates=["Timestamp"])
viz_df = df[["Timestamp", "cpu_usage_idle", "mem_used_percent"]].tail(1000).copy()

viz_df["cpu_usage"] = 100 - viz_df["cpu_usage_idle"]

viz_df = viz_df.sort_values("Timestamp")

plt.figure(figsize=(14, 6))
plt.plot(viz_df["Timestamp"], viz_df["mem_used_percent"], label="RAM-Auslastung (%)", color="darkorange")
plt.plot(viz_df["Timestamp"], viz_df["cpu_usage"], label="CPU-Auslastung (%)", color="royalblue")
plt.xlabel("Zeitstempel")
plt.ylabel("Auslastung (%)")
plt.title("CPU- und RAM-Auslastung im Zeitverlauf")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
