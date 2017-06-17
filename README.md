![Elasticsearch Synonyms](docs/banner.png)

[![Build Status][travis-img-url]][travis-href]
[![PyPI Version][pypi-v-shield-url]][pypi-href]

This repository contains a curated dataset of synonyms in [Solr Format][1]. These
synonyms can be used for [Elasticsearch Synonym Token Filter][2] configuration.

Additional helper tools in this repository:

- `synlint`: Commandline tool to lint and validate the synonym files.
- `synonyms.sublime-syntax`: Syntax highlighting file for Sublime Text 3.


## Datasets

The synonym files in `data/` can be used directly in elasticsearch configuration.

Following datasets are currently available:
- `be-ae`: British English and American English Spellings. From [AVKO.org](https://to.noop.pw/2sNor7C).

## Installation

If you want to use the `synlint` tool, install the package from PIP using:
```shell
pip install elasticsearch-synonym-toolkit
```

This will install a linter tool, `es-synlint`. Use it with:

```shell
es-synlint [synonymfile]
```

## Development

- Clone this repository.
- Install package dependencies via `pip` with: `pip install -r requirements.txt`.
- To run tests:
```shell
./panda test:all
```

## License

The tools and codes are licensed under MIT.
The datasets are used under fair use and are derivative of the original sources. 

[1]: https://cwiki.apache.org/confluence/display/solr/Filter+Descriptions#FilterDescriptions-SynonymFilter
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html#analysis-synonym-tokenfilter
[travis-img-url]: https://travis-ci.org/prashnts/elasticsearch-synonyms.svg?branch=master
[travis-href]: https://travis-ci.org/prashnts/elasticsearch-synonyms
[pypi-href]: https://pypi.python.org/pypi/elasticsearch-synonym-toolkit
[pypi-v-shield-url]: https://img.shields.io/pypi/v/elasticsearch-synonym-toolkit.svg
