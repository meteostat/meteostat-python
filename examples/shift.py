import pandas as pd

# Your first DataFrame
df1 = pd.DataFrame(
    {
        "temp": [7.0, 6.9, 6.6, 7.0, 7.0],
        "rhum": [79, 78, 86, 81, 79],
        "prcp": [0.0, 0.0, 0.2, 0.0, 0.0],
        "snwd": [0, 0, 0, 0, 0],
        "wdir": [210, 200, 200, 200, 210],
        "wspd": [22.3, 20.5, 19.8, 20.5, 24.5],
        "wpgt": [32.0, 33.0, 35.0, 33.0, 40.0],
        "pres": [1006.4, 1006.6, 1006.9, 1006.7, 1006.8],
        "tsun": [0, 0, 0, 0, 0],
        "cldc": [8, 8, 8, 7, 7],
        "coco": [8, 7, 8, 7, 8],
    },
    index=pd.MultiIndex.from_arrays(
        [
            [10637] * 5,
            pd.date_range("2024-01-01", periods=5, freq="h"),
            ["bulk_hourly"] * 5,
        ],
        names=["station", "time", "source"],
    ),
)

# Your second DataFrame
df2 = pd.DataFrame(
    {
        "temp": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "rhum": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "prcp": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "snwd": ["synop", "synop", "synop", "synop", "synop"],
        "wdir": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "wspd": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "wpgt": ["synop", "synop", "synop", "synop", "synop"],
        "pres": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "tsun": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "cldc": ["dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly", "dwd_hourly"],
        "coco": ["dwd_hourly", "synop", "dwd_hourly", "synop", "dwd_hourly"],
    },
    index=pd.date_range("2024-01-01", periods=5, freq="h"),
)

# Reshape df1 to long format
df1_long = df1.reset_index().melt(
    id_vars=["station", "time", "source"], var_name="param"
)

# Reshape df2 to long format
df2_long = df2.reset_index().melt(var_name="param")

# Initialize an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

# Iterate over each parameter and merge the data
for param in df1_long["param"].unique():
    temp_df = pd.merge(
        df1_long[df1_long["param"] == param],
        df2_long[df2_long["param"] == param],
        on=["time", "param"],
        suffixes=("", "_source"),
    )
    temp_df.drop(columns=["source", "param"], inplace=True)
    merged_df = pd.concat([merged_df, temp_df], axis=0)

# Pivot merged DataFrame to wide format
final_df = merged_df.pivot_table(
    index=["station", "time", "source"], columns="param", values="value"
)

print(final_df)
