# Data Quality

When working with weather and climate data it is important to know which quality standards are used by the providers and weather station operators. While some things are standardized, others are handled differently across the involved organizations.

## Instruments & Measurements

Meteostat cannot always tell for sure which quality standards were used in each and every step of the process. That is because Meteostat does not operate weather stations itself. Therefore, we cannot tell which instruments are used to measure meteorological parameters at the different weather stations. You can think of Meteostat as a _"Google for meteorological data"_. We collect and redistribute data which was observed by national weather services across the world. Similarly to Google, which is not responsible for the content of all the websites it links to, we can take certain actions to ensure the quality of our information, but in the end we rely on the QA processes of the national weather services which gather and provide data.

All weather stations available through Meteostat **follow the international WMO standards**. If you want to learn more about the standards of a national weather service, please reach out to them directly.

## Observations vs. Model Data

When using any Meteostat product, you will see a mix of real observations and model data by default. Weather models are generally used to provide analysis and forecasts for any geographical location. While the spatial resolution is a huge advantage of model data, it cannot compete with real observations. Especially, when it comes to local precipitation events and thunderstorms. As Meteostat's main focus is a good user experience, we show you all available data by default.

If you only want to work with observation data, Meteostat always allows you to opt-out of model data. Please read the respective interface documentation for more information.

## Observation Quality

Meteostat uses different sources for weather observations. If available, we show the official observations published by the national weather service of the respective country. Alternatively, we will utilize international historical databases. Next in line are synoptic observations and METAR reports. Only if all these sources fail to provide data, Meteostat will fall back to model data.

All of these interfaces use different formats, units and standards. For example, the measurements of METAR reports are typically rounded to full integer values. Therefore, it might well be that two datasets are based on the same observation, but differ mathematically.

## Aggregation Methods

Another common source of confusion are aggregation methods. Is the average temperature of the day the true average, mean or median? Which time zone is used to calculate the averages? Which observation frequency is used as raw data for aggregations?

That is where things get complicated. Some weather services base daily averages on certain points of time throughout the day. Others use continuous time series with a frequency of five minutes. For our own daily aggregations we strictly use 24 hourly data points.

It is a fact: we do not always know for sure which method was used by a data provider. Therefore, please consider carefully which degree of accuracy you need for your use case. Never trust data blindly - no matter where it comes from!

## Wrap Up

Most data provided by Meteostat can be considered accurate. It is coming from official weather services around the world and follows high standards. However, you will probably encounter small inconsistencies from time to time when working with Meteostat data. For most use cases, these inconsistencies do not matter. If you are doing predictive analytics in a sales unit, it probably does not matter if a day's average temperature was 23.3 °C or 23.4 °C. But especially scientific use cases sometimes require super-accurate data. In such cases, you should probably perform additional quality checks.

As you can see, the truth is sometimes relative. Therefore, in case of doubt please keep it like Winston Churchill:

> The only statistics you can trust are those you falsified yourself.

By the way: You can help Meteostat improve its data quality by making a [contribution](/contributing).
