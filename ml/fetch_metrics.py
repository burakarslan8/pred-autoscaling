import boto3
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def fetch_metric(metric_name, dimensions, start_time, end_time, period=60):
    client = boto3.client('cloudwatch', region_name='eu-central-1')
    response = client.get_metric_statistics(
        Namespace='CWAgent',
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=['Average']
    )
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        logging.warning(f"No data for: {metric_name} ({start_time} - {end_time})")
        return pd.DataFrame()
    df = pd.DataFrame([{
        'Timestamp': dp['Timestamp'],
        metric_name: dp['Average']
    } for dp in datapoints])
    return df.sort_values(by='Timestamp')

def main():
    instance_id = 'i-0c113edd28790e2b3'
    metrics = {
        'cpu_usage_idle': [
            {'Name': 'InstanceId', 'Value': instance_id},
            {'Name': 'cpu', 'Value': 'cpu-total'}
        ],
        'cpu_usage_iowait': [
            {'Name': 'InstanceId', 'Value': instance_id},
            {'Name': 'cpu', 'Value': 'cpu-total'}
        ],
        'mem_used_percent': [
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        'swap_used_percent': [
            {'Name': 'InstanceId', 'Value': instance_id}
        ],
        'diskio_io_time': [
            {'Name': 'InstanceId', 'Value': instance_id},
            {'Name': 'name', 'Value': 'nvme0n1'}
        ]
    }

    end_time = datetime.utcnow()
    days = 7
    all_data = []

    for day in range(days):
        day_start = end_time - timedelta(days=(day + 1))
        day_end = end_time - timedelta(days=day)
        merged_day_df = None

        for metric_name, dims in metrics.items():
            df = fetch_metric(metric_name, dims, start_time=day_start, end_time=day_end)
            if df.empty:
                continue
            if merged_day_df is None:
                merged_day_df = df
            else:
                merged_day_df = pd.merge(merged_day_df, df, on='Timestamp', how='outer')

        if merged_day_df is not None:
            all_data.append(merged_day_df)

    if all_data:
        final_df = pd.concat(all_data).sort_values(by='Timestamp')
        final_df.to_csv('cloudwatch_metrics.csv', index=False)
        logging.info("Data saved: cloudwatch_metrics.csv")
    else:
        logging.warning("No data pulled.")

if __name__ == '__main__':
    main()
