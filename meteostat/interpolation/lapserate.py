from itertools import combinations
from typing import List
import numpy as np
import pandas as pd

from meteostat.core.config import config
from meteostat.enumerations import Parameter


def apply_static_lapse_rate(
    df: pd.DataFrame, elevation: int, lapse_rate: float
) -> pd.DataFrame:
    """
    Calculate approximate temperature at target elevation
    using a given lapse rate.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be adjusted.
    elevation : int
        Target elevation in meters.
    lapse_rate : float
        Lapse rate (temperature gradient) in degrees Celsius per kilometer.

    Returns
    -------
    pd.DataFrame
        DataFrame with adjusted temperature values.
    """
    columns = config.get(
        "interpolation.lapse_rate.cols",
        [
            Parameter.TEMP,
            Parameter.TMIN,
            Parameter.TMAX,
        ],
    )

    for col in columns:
        if col in df.columns:
            df.loc[df[col] != np.nan, col] = round(
                df[col] + ((lapse_rate / 1000) * (df["elevation"] - elevation)), 1
            )

    return df

def calculate_dynamic_lapse_rate(
    df: pd.DataFrame,
    parameters: List[Parameter] = [],
) -> pd.DataFrame:
    """
    Calculate dynamic lapse rates for specified parameters.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data with MultiIndex (station, time).
    parameters : list of Parameter, optional
        List of parameters to calculate lapse rates for.

    Returns
    -------
    pd.DataFrame
        DataFrame with calculated lapse rates per 100 meters.
    """
    if df.empty or 'elevation' not in df.columns:
        return None
    
    # Get elevation per station (take the first non-null elevation for each station)
    elev_by_station = df["elevation"].groupby(level="station").first()

    results = {}

    # Unstack so we have times as index and stations as columns for each variable
    # We'll use df[parameter].unstack(level=station_level) for each variable
    for parameter in filter(lambda p: p in df.columns, parameters):
        unstacked = df[[parameter]].unstack(level="station")  # DataFrame with columns like (var, station)
        # After unstack, columns is a MultiIndex (var, station). Extract station level.
        # Simpler: get unstacked[parameter] returns DataFrame time x station
        if isinstance(unstacked.columns, pd.MultiIndex):
            df_var = unstacked[parameter]
        else:
            # If only one station, unstack might produce single-level columns
            df_var = unstacked

        stations = list(df_var.columns)
        # align elevations to the station columns (stations might be strings)
        try:
            elevs = elev_by_station.loc[stations]
        except KeyError:
            # if some stations missing elevation, attempt to coerce types, else raise
            elevs = elev_by_station.reindex(stations)
        # Prepare list to collect per-pair series
        pair_series = []

        # iterate all unique station pairs
        for a, b in combinations(stations, 2):
            if pd.isna(elevs[a]) or pd.isna(elevs[b]) or elevs[a] == elevs[b]:
                continue
            # slope series for this pair (absolute temperature difference per 100 m)
            s = (df_var[a] - df_var[b]) / (float(elevs[a]) - float(elevs[b])) * 100.0
            # name column for debugging / optional inspection
            s.name = f"{a}__{b}"
            pair_series.append(s)

        if not pair_series:
            # no valid pairs -> fill NaN
            results[parameter] = pd.Series(index=df_var.index, dtype=float)
        else:
            slopes_df = pd.concat(pair_series, axis=1)
            # median across station-pairs for each time
            results[parameter] = slopes_df.median(axis=1, skipna=True)

    result_df = pd.DataFrame(results)
    result_df.index.name = "time"
    return result_df

def apply_dynamic_lapse_rate(
    df: pd.DataFrame,
    parameters: List[Parameter] = [],
) -> pd.DataFrame:
    """
    Apply dynamic lapse rate correction based on elevation difference.

    This function calculates the lapse rate dynamically using available data
    and applies it to the specified parameters for each time step. If a 
    target_elevation is provided, the lapse rate is scaled by the elevation 
    difference between each station and the target elevation.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data to be adjusted with MultiIndex (station, time).
        Must contain 'elevation' column and meteorological parameters.
    parameters : list of Parameter, optional
        List of parameters to apply lapse rate correction to (default: None,
        which applies to all temperature-related parameters).
    target_elevation : int, float, or None, optional
        Target elevation in meters. If provided, lapse rates will be scaled
        by the elevation difference between each station and this target.
        If None, will attempt to use 'elevation_difference' or 'elevation_diff' 
        columns if available.

    Returns
    -------
    pd.DataFrame
        DataFrame with adjusted values based on dynamic lapse rates, scaled
        by elevation difference if available.
    """
    lapse_rates_df = calculate_dynamic_lapse_rate(df, parameters)

    if lapse_rates_df is None or lapse_rates_df.empty:
        return df

    # Create a copy to avoid modifying the original DataFrame
    df_adjusted = df.copy()

    # Determine how to calculate elevation scaling
    elevation_scaling = df_adjusted["elevation_diff"] / 100.0

    # Apply the calculated lapse rates to the DataFrame
    for param in parameters:
        if param not in lapse_rates_df.columns:
            continue

        # Get the lapse rate series for this parameter
        lapse_rate_series = lapse_rates_df[param]

        if elevation_scaling is not None:
            # Scale the lapse rate by elevation difference (lapse rate is per 100m)
            scaled_lapse_rate = lapse_rate_series * elevation_scaling
            
            # Apply the scaled lapse rate adjustment
            df_adjusted[param] = df_adjusted[param] + scaled_lapse_rate
        else:
            # Fallback to original behavior if no elevation scaling available
            df_adjusted[param] = df_adjusted[param] + lapse_rate_series

    return df_adjusted
