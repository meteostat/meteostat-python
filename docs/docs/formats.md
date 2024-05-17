# Formats & Units

## Date & Time

Date and time statements follow the ISO 8601 standard (e.g. _2016-12-31_ for _December 31st 2016_ and _23:59:58_ for _23 hours, 59 minutes, and 58 seconds_). The time zone used by Meteostat is Coordinated Universal Time (UTC).

## Meteorological Parameters

Meteostat uses abbreviations to describe meteorological parameters. A bold **yes** means that the parameter is a key parameter which is included in Meteostat's data mirror. If it's marked with an asterisk (*), the parameter is derived from one or multiple other parameter(s).

| **Code** | **Description**         | **Hourly** | **Daily** |
| :------- | :---------------------- | :--------- | :-------- |
| TEMP     | Air Temperature         | **Yes**    |      No   |
| TAVG     | Average Temperature     | No    |      **Yees**   |
| TMIN     | Minimum Temperature     | No    |      **Yees**   |
| TMAX     | Maximum Temperature     | No    |      **Yees**   |
| DWPT     | Dew Point               | **Yes***    |      No   |
| PRCP     | Total Precipitation     | **Yes**    |      **Yees**   |
| WDIR     | Wind (From) Direction   | **Yes**    |      No   |
| WSPD     | Average Wind Speed      | **Yes**    |      No   |
| WPGT     | Wind Peak Gust          | **Yes**    |      No   |
| RHUM     | Relative Humidity       | **Yes**    |      No   |
| PRES     | Sea-Level Air Pressure  | **Yes**    |      No   |
| SNOW     | Snow Depth              | **Yes**    |      No   |
| TSUN     | Total Sunshine Duration | **Yes**    |      No   |
| COCO     | Weather Condition Code  | **Yes**    |      No   |


## Weather Condition Codes

Hourly weather data may include information on the observed weather condition. Please note that the weather condition is not a key parameter for Meteostat. METAR reports, issued by weather stations located at airports, only report significant weather events. Also, some weather stations do not provide weather condition data at all.

Weather conditions are indicated by an integer value between 1 and 27 according to this list:

| **Code** | **Weather Condition** |
| :------- | :-------------------- |
| 1        | Clear                 |
| 2        | Fair                  |
| 3        | Cloudy                |
| 4        | Overcast              |
| 5        | Fog                   |
| 6        | Freezing Fog          |
| 7        | Light Rain            |
| 8        | Rain                  |
| 9        | Heavy Rain            |
| 10       | Freezing Rain         |
| 11       | Heavy Freezing Rain   |
| 12       | Sleet                 |
| 13       | Heavy Sleet           |
| 14       | Light Snowfall        |
| 15       | Snowfall              |
| 16       | Heavy Snowfall        |
| 17       | Rain Shower           |
| 18       | Heavy Rain Shower     |
| 19       | Sleet Shower          |
| 20       | Heavy Sleet Shower    |
| 21       | Snow Shower           |
| 22       | Heavy Snow Shower     |
| 23       | Lightning             |
| 24       | Hail                  |
| 25       | Thunderstorm          |
| 26       | Heavy Thunderstorm    |
| 27       | Storm                 |