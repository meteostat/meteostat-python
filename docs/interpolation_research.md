# Spatial Interpolation Methods for Weather Data

## Overview

This document outlines the research and design decisions for implementing spatial interpolation methods for point-based weather data in the Meteostat Python library.

## Background

Weather data is collected at discrete weather stations, but users often need data at specific geographic locations where no station exists. Spatial interpolation estimates values at unmeasured locations based on values from nearby stations.

## Interpolation Methods

### 1. Nearest Neighbor (Already Implemented)

**Method**: Uses the value from the closest weather station.

**Advantages**:
- Simple and fast
- Preserves actual measured values
- No assumptions about spatial correlation

**Disadvantages**:
- Discontinuous (abrupt changes at boundaries)
- Ignores information from other nearby stations
- Can be inaccurate if nearest station is far or at different elevation

**Use Case**: When the nearest station is very close (<5km) and at similar elevation (<50m difference).

**References**:
- Gold, C. M. (1989). "Surface interpolation, spatial adjacency and GIS". Three Dimensional Applications in GIS.

### 2. Inverse Distance Weighting (IDW)

**Method**: Estimates values as a weighted average of nearby stations, where weights decrease with distance.

**Formula**:
```
Z(x) = Σ(wi * Zi) / Σ(wi)
where wi = 1 / (di^p)
```
- Z(x) = interpolated value at location x
- Zi = value at station i
- di = distance from x to station i
- p = power parameter (typically 2)

**With Elevation Consideration**:
We use a modified distance metric that incorporates both horizontal distance and elevation difference:

```
effective_distance = sqrt(horizontal_distance^2 + (elevation_diff * elevation_weight)^2)
```

**Advantages**:
- Smooth interpolation
- Considers multiple nearby stations
- Well-established method in meteorology
- Can incorporate elevation differences

**Disadvantages**:
- Can oversmooth data
- Sensitive to power parameter choice
- May not capture local variations well

**Use Case**: General-purpose interpolation when multiple stations are available within reasonable distance.

**References**:
- Shepard, D. (1968). "A two-dimensional interpolation function for irregularly-spaced data". Proceedings of the 1968 ACM National Conference.
- Ly, S., Charles, C., & Degré, A. (2011). "Geostatistical interpolation of daily rainfall at catchment scale: the use of several variogram models in the Ourthe and Ambleve catchments, Belgium". Hydrology and Earth System Sciences, 15(7), 2259-2274.

### 3. Random Forest Regression (RFR) Interpolation

**Method**: Uses scikit-learn's RandomForestRegressor trained on spatial features to predict weather values at unmeasured locations.

**Features**:
- Latitude
- Longitude  
- Elevation (when available)

**Model**: Random Forest Regressor
- Ensemble of decision trees that vote on predictions
- Handles non-linear relationships naturally
- Robust to outliers
- Can capture complex spatial patterns
- No assumptions about data distribution

**Training Approach**:
- For each time step, train a separate model for each weather parameter
- Use nearby station data as training samples
- Features: geographic coordinates and elevation
- Target: weather parameter value at that location

**Advantages**:
- Can capture complex spatial relationships that linear methods miss
- Automatically learns importance of elevation and location
- Handles non-stationarity in spatial patterns
- Generally more accurate than distance-based methods
- Works well even with limited training data

**Disadvantages**:
- Requires scikit-learn installation
- More computationally expensive than IDW
- Less interpretable than distance-based methods
- Requires at least 2 stations for training

**Use Case**: When highest accuracy is needed and computational cost is acceptable. Especially useful in complex terrain.

**Implementation Note**: This method is loaded dynamically so that scikit-learn remains an optional dependency. Users only need to install it if they want to use RFR interpolation.

**References**:
- Hengl, T., Nussbaum, M., Wright, M. N., Heuvelink, G. B., & Gräler, B. (2018). "Random forest as a generic framework for predictive modeling of spatial and spatio-temporal variables". PeerJ, 6, e5518. https://doi.org/10.7717/peerj.5518
- Sekulić, A., Kilibarda, M., Heuvelink, G. B., Nikolić, M., & Bajat, B. (2020). "Random Forest Spatial Interpolation". Remote Sensing, 12(10), 1687. https://doi.org/10.3390/rs12101687
- RFSI implementation: https://github.com/AleksandarSekulic/RFSI

### 4. Auto (Hybrid Approach)

**Method**: Intelligently selects between Nearest Neighbor and IDW based on spatial context.

**Decision Logic**:
```
IF nearest_station_distance <= 5000m AND elevation_difference <= 50m:
    USE nearest_neighbor
ELSE:
    USE IDW with elevation weighting
```

**Rationale**:
- When a very close station exists at similar elevation, its measurement is likely most accurate
- For more distant stations or significant elevation differences, averaging multiple stations (IDW) is better
- Balances accuracy and computational efficiency

**Advantages**:
- Adaptive to local conditions
- Simple and interpretable
- Good default choice
- Fast

**Disadvantages**:
- Arbitrary thresholds (though based on meteorological principles)
- May not be optimal in all cases

**Use Case**: Default method for general-purpose interpolation when scikit-learn is not available or when speed is prioritized over maximum accuracy.

**References**:
- Willmott, C. J., & Robeson, S. M. (1995). "Climatologically aided interpolation (CAI) of terrestrial air temperature". International Journal of Climatology, 15(2), 221-229.

## Elevation Considerations

Weather variables, especially temperature, are strongly correlated with elevation. The standard environmental lapse rate is approximately 6.5°C per 1000m elevation gain.

**Implementation**:
1. For temperature variables, apply lapse rate adjustment (already implemented)
2. For IDW, use 3D distance metric that weights elevation difference
3. For ML methods, include elevation as a key feature

**References**:
- Barry, R. G. (2008). "Mountain Weather and Climate" (3rd ed.). Cambridge University Press.
- Dodson, R., & Marks, D. (1997). "Daily air temperature interpolated at high spatial resolution over a large mountainous region". Climate Research, 8(1), 1-10.

## Performance Benchmarks

Benchmarks should compare:
- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)
- Computational time
- Memory usage

Test locations:
- Frankfurt, Germany (flat terrain)
- Denver, USA (mountainous)
- Singapore (tropical coastal)
- Multiple weather variables (temp, precipitation, etc.)

## Implementation Notes

1. All methods should handle missing data gracefully
2. Methods should work with both single points and multiple points
3. Performance should be optimized for typical use cases (1-10 nearby stations)
4. API should allow custom interpolation functions for advanced users

## Conclusion

Each interpolation method has trade-offs. The "Auto" method provides a good default, while specialized methods (IDW, ML) offer improvements for specific use cases. The implementation provides flexibility while maintaining ease of use.
