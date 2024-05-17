# Contribute

Meteostat is an open initiative which does not operate on a primarily commercial basis. We believe that weather and climate data should be freely available to everyone. Therefore, Meteostat operates multiple interfaces which provide free access to meteorological data. Operating, maintaining and growing the project is only possible with the help of people like you.

This section contains information about how to contribute to Meteostat. It also defines general principles and concepts which serve as a foundation for the project and its architecture.

If you want to support Meteostat on its mission of making weather and climate data available to everyone, you have multiple options to choose from:

* Contribute to our open source repositories on [GitHub](https://github.com/meteostat)
* Spread the news about Meteostat on social media or your website
* Make a [donation](/contributing.html#donations)

Meteostat's goal is to publish the majority of its coding under the MIT license on [GitHub](https://github.com/meteostat). Feel free to open an issue if you run into a bug or create a pull request for new features and fixes.

## Weather Stations

Meteostat provides an open directory of weather stations everyone can edit, share and build upon. The list of weather stations is available on [GitHub](https://github.com/meteostat/weather-stations).

If you want to add a missing station, please create a new file in the `stations` folder according to the template described [here](https://github.com/meteostat/weather-stations#properties). If possible, please to also add the weather station to the CSV files in [this directory](https://github.com/meteostat/routines/tree/master/resources). Adding the corresponding identifier to the CSV files will make sure all available data is collected properly.

### Joining Stations

It can happen that the same weather station appears twice under different IDs. In this case, all duplicates should be unified in a single JSON file under a common identifier.

1. Pick one of the existing JSON files.
2. Add all identifiers and details available for this weather station. In case of inconsistencies, do some research or open an issue.
3. Delete all duplicates.
5. Create a pull request.

## Data Routines

All automated routines, for both import & export of data, are available [here](https://github.com/meteostat/routines). By adding new data sources, you can help Meteostat improve its data coverage.

## Python Library

Please refer to [this page](/python/contributing).

## Documentation

Last but not least, this documentation is an [open source project](https://github.com/meteostat/dev), too. Keeping our docs up-to-date is crucial. If you are contributing to parts of our ecosystem, please make sure to add corresponding documentation. Also, if anything appears to be unclear or misleading in one of our articles, feel free to propose changes.

The Meteostat team will review all pull requests. Once a PR has been approved and merged into the `master` branch, Meteostat will automatically deploy changes into the productive environment.
