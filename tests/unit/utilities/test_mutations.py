"""
Unit Test - Mutations Module

Tests for the mutations utility functions.

The code is licensed under the MIT license.
"""

import pandas as pd
import numpy as np
from meteostat.utilities.mutations import calculate_dwpt


def test_calculate_dwpt_with_missing_columns():
    """
    Test: calculate_dwpt() with missing required columns
    
    When the dataframe doesn't have the required 'temp' or 'rhum' columns,
    the function should return the dataframe unchanged without raising a KeyError.
    """
    
    # Create an empty dataframe
    df = pd.DataFrame()
    result = calculate_dwpt(df, "dwpt")
    assert result.equals(df)
    
    # Create a dataframe with only temp column
    df_temp_only = pd.DataFrame({"temp": [20.0, 21.0, 22.0]})
    result = calculate_dwpt(df_temp_only, "dwpt")
    assert result.equals(df_temp_only)
    assert "dwpt" not in result.columns
    
    # Create a dataframe with only rhum column
    df_rhum_only = pd.DataFrame({"rhum": [80.0, 85.0, 90.0]})
    result = calculate_dwpt(df_rhum_only, "dwpt")
    assert result.equals(df_rhum_only)
    assert "dwpt" not in result.columns


def test_calculate_dwpt_with_valid_columns():
    """
    Test: calculate_dwpt() with valid required columns
    
    When the dataframe has both 'temp' and 'rhum' columns,
    the function should calculate the dew point temperature.
    """
    
    # Create a dataframe with both required columns
    df = pd.DataFrame({
        "temp": [20.0, 15.0, 10.0],
        "rhum": [80.0, 70.0, 60.0],
        "temp_flag": ["A", "A", "B"],
        "rhum_flag": ["A", "B", "A"]
    })
    
    result = calculate_dwpt(df, "dwpt")
    
    # Check that dwpt column was added
    assert "dwpt" in result.columns
    assert "dwpt_flag" in result.columns
    
    # Check that dwpt values are numeric and rounded to 1 decimal
    assert result["dwpt"].dtype == "float64"
    assert all(result["dwpt"].round(1) == result["dwpt"])
    
    # Check that dwpt_flag was calculated from temp_flag and rhum_flag
    assert result["dwpt_flag"].tolist() == ["A", "B", "B"]
