# Mkdocs Protobuf plugin

<p align="center">
    <em></em>
</p>

[![build](https://github.com/rymurr/mkdocs_protobuf/workflows/Build/badge.svg)](https://github.com/rymurr/mkdocs_protobuf/actions)
[![codecov](https://codecov.io/gh/rymurr/mkdocs_protobuf/branch/master/graph/badge.svg)](https://codecov.io/gh/rymurr/mkdocs_protobuf)
[![PyPI version](https://badge.fury.io/py/mkdocs_protobuf.svg)](https://badge.fury.io/py/mkdocs_protobuf)

---

**Source Code**: <a href="https://github.com/rymurr/mkdocs_protobuf" target="_blank">https://github.com/rymurr/mkdocs_protobuf</a>

---

This plugin inserts protobuf messages into template parameters in mkdocs websites. It can be
used to embed Protobuf IDL into documentation sites.

## Usage

To use in mkdocs install via pip `pip install mkdocs_protobuf`.

Add the following to `mkdocs.yml`

```
plugins:
 - mkdocs_protobuf:
     proto_dir: /path/to/proto/files
```

The plugin will search for any templataes like the following: `%%% proto.message.MessageName %%%`
and will replace the template with the protobuf message `MessageName`. See the `tests` directory
for an example. The escape characters are odd as to not interfere w/ Jinja2 templating from other plugins.


## Development

### Setup environement

You should have [Pipenv](https://pipenv.readthedocs.io/en/latest/) installed. Then, you can install the dependencies with:

```bash
pipenv install --dev
```

After that, activate the virtual environment:

```bash
pipenv shell
```

### Run unit tests

You can run all the tests with:

```bash
make test
```

Alternatively, you can run `pytest` yourself:

```bash
pytest
```

### Format the code

Execute the following command to apply `isort` and `black` formatting:

```bash
make format
```

## License

This project is licensed under the terms of the Apache Software License 2.0.
