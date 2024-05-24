# Caching

All function which load and/or parse data should be annotated with the `cache` decorator.

When creating a new provider, we will have a file handler which is responsible for downloading, parsing and cleaning the data. Consider the example of GHCND data. This provider will have a `file_handler` which takes the GHCND station ID. This file handler returns a DF which holds all data for all parameters Meteostat supports. Only parameters which are not supported by Meteostat are dropped from the DF. The DF will be cached as Pickle.

The `data_handler` will call the `file_handler` and it will clean the resulting DF to match exactly the user's request. E.g. it will drop all rows which are not in the time range.