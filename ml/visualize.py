import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("final_dataset.csv", parse_dates=["Timestamp"])
viz_df = df[["Timestamp", "cpu_usage_idle", "mem_used_percent", "scaling_decision"]].copy()

viz_df["cpu_usage"] = 100 - viz_df["cpu_usage_idle"]
viz_df = viz_df.sort_values("Timestamp")

first_monday = viz_df["Timestamp"].dt.normalize().loc[viz_df["Timestamp"].dt.weekday == 0].min()
last_sunday = first_monday + pd.Timedelta(days=6, hours=23, minutes=59)
viz_df_week = viz_df[(viz_df["Timestamp"] >= first_monday) & (viz_df["Timestamp"] <= last_sunday)]

viz_df_week = viz_df_week.set_index("Timestamp")
numeric_cols = ["cpu_usage_idle", "mem_used_percent", "cpu_usage"]
viz_df_num = viz_df_week[numeric_cols].resample("30min").mean().reset_index()

plt.figure(figsize=(16, 6))
plt.plot(viz_df_num["Timestamp"], viz_df_num["cpu_usage"], label="CPU-Auslastung (%)", color="royalblue")
plt.plot(viz_df_num["Timestamp"], viz_df_num["mem_used_percent"], label="RAM-Auslastung (%)", color="darkorange", linewidth=2)
plt.xlabel("Zeitstempel")
plt.ylabel("Auslastung (%)")
plt.title("CPU- und RAM-Auslastung (Eine Woche ab Montag, 30 Min Sampling)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
