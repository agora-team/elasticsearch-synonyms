![Elasticsearch Synonyms](docs/banner.png)

This repository contains a curated dataset of synonyms in [Solr Format][1]. These
synonyms can be used for [Elasticsearch Synonym Token Filter][2] configuration.

Additional helper tools in this repository:

- `synlint`: Commandline tool to lint and validate the synonym files.
- `synonyms.sublime-syntax`: Syntax highlighting file for Sublime Text 3.


## Datasets

Following datasets are currently available:
- `be-ae`: British English and American English Spellings. From [AVKO.org](https://to.noop.pw/2sNor7C).

## Usage

- The synonym files in `data/` can be used directly in configuration.
- To use the linter tool, install python dependencies from `requirements.txt` and use:
```shell
python -m synlint [file names]
```
- To run tests:
```shell
./panda test:all
```

## License

The tools and codes are licensed under MIT.
The datasets are used under fair use and derivative of the original sources. 

[1]: https://cwiki.apache.org/confluence/display/solr/Filter+Descriptions#FilterDescriptions-SynonymFilter
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html#analysis-synonym-tokenfilter
