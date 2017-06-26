![Elasticsearch Synonyms](docs/banner.png)

[![Build Status][travis-img-url]][travis-href]
[![PyPI Version][pypi-v-shield-url]][pypi-href]

This repository contains a curated dataset of synonyms in [Solr Format][1]. These
synonyms can be used for [Elasticsearch Synonym Token Filter][2] configuration.

Additional helper tools in this repository:

- `synlint`: Commandline tool to lint and validate the synonym files.
- `synonyms.sublime-syntax`: Syntax highlighting file for Sublime Text 3.

If you're using Elasticssearch with Django, you might find [`dj-elasticsearch-flex`][es_flex] useful.

## Why?

Trying to configure Synonyms in Elasticsearch, I found that docs for it are surprisingly scattered.
The docs that are available do not do much justice either and miss out many corner cases.

For instance, an incorrect Solr mapping: `hello, world,` would be happily added in index configuration.
However, as soon as you'd try to re-open the index, you'd get a `malform_input_exception` [(discussion thread)][4].

This repository solves such problems by with a linter tool that can be used to validate the synonym
files beforehand.

## Datasets

The synonym files in `data/` can be used directly in elasticsearch configuration.

Following datasets are currently available:
- `be-ae`: British English and American English Spellings. From [AVKO.org](https://to.noop.pw/2sNor7C).

## Installation

If you want to use the `synlint` tool, install the package from PIP using:
```shell
pip install elasticsearch-synonym-toolkit
```

The Python Package is installed as `es_synonyms`. This will also install a linter tool,
`es-synlint`. Use it with:

```shell
es-synlint [synonymfile]
```

## Usage

In most cases, you'd want to use this module as a helper for loading validated synonyms from a file or a url:
```python
from es_synonyms import load_synonyms

# Load synonym file at some URL:
be_ae_syns = load_synonyms('https://to.noop.pw/2sI9x4s')
# Or, from filesystem:
other_syns = load_synonyms('data/be-ae.synonyms')
```

Configuring [Synonym Tokenfilter][2] with [Elasticsearch DSL Py][3], is very easy, too:
```python
from elasticsearch_dsl import analyzer, token_filter

be_ae_syns = load_synonyms('https://to.noop.pw/2sI9x4s')

# Create a tokenfilter
brit_spelling_tokenfilter = token_filter(
  'my_tokenfilter',     # Any name for the filter
  'synonym',            # Synonym filter type
  synonyms=be_ae_syns   # Synonyms mapping will be inlined
)
# Create analyzer
brit_english_analyzer = analyzer(
  'my_analyzer',
  tokenizer='standard',
  filter=[
    'lowercase',
    brit_spelling_tokenfilter
  ])
```

To use the underlying linter, you can import `SynLint` class.

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
[3]: https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html#analysis
[4]: https://discuss.elastic.co/t/synonym-using-a-file-is-not-working-malformed-input-exception/60487
[es_flex]: https://github.com/prashnts/dj-elasticsearch-flex
[travis-img-url]: https://travis-ci.org/prashnts/elasticsearch-synonyms.svg?branch=master
[travis-href]: https://travis-ci.org/prashnts/elasticsearch-synonyms
[pypi-href]: https://pypi.python.org/pypi/elasticsearch-synonym-toolkit
[pypi-v-shield-url]: https://img.shields.io/pypi/v/elasticsearch-synonym-toolkit.svg
