# Meteostat Python Package

This is the development branch for Meteostat 2.0.0.

## Running Scripts

```sh
poetry run python3 examples/test.py
```

## Auto Formatting

TODO: Use dev dep

```sh
poetry run black .
```

## Logging

You can change the default log level, format etc. using the `logging` package:

```py
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(filename)s:%(lineno)s] %(message)s')
```

## Testing

Run the following command for unit tests:

```sh
poetry run pytest tests/unit
```

Run the following command for integration tests:

```sh
poetry run pytest tests/integration
```

Run the following command for system tests (involves network requests):

```sh
poetry run pytest tests/system
```

Run the following command for provider tests (involves network requests):

```sh
poetry run pytest tests/provider
```

## Config

### Using Environment Variables

Enable debug mode:

```sh
export METEOSTAT_DEBUG=1
```

Disable auto-cleaning:

```sh
export METEOSTAT_CACHE_AUTOCLEAN=
```