import pytest
import os

from es_synonyms import parser, SynParser, load_synonyms
from es_synonyms import exceptions

def test_parse_empty_line():
  assert parser.empty_line(' ') is True
  assert parser.empty_line('\n') is True
  assert parser.empty_line('42') is None

def test_parse_comment_line():
  assert parser.comment_line('# 42') is True
  assert parser.comment_line('42') is None

def test_parse_mapping_line():
  assert parser.mapping_line('42') is True
  assert parser.mapping_line('42, 44') is True
  assert parser.mapping_line('a => b') is True
  assert parser.mapping_line('a, b => c, d') is True
  assert parser.mapping_line('a, b => c') is True

def test_parse_mapping_line_trailing_comma():
  with pytest.raises(exceptions.ParserError):
    assert parser.mapping_line('a, => b')

  with pytest.raises(exceptions.ParserError):
    assert parser.mapping_line('a, b => b, c,')

  with pytest.raises(exceptions.ParserError):
    assert parser.mapping_line('a,')

def test_parse_mapping_line_unbalanced_tokens():
  with pytest.raises(exceptions.ParserWarning):
    parser.mapping_line('a, b => c, d, e')

def test_parse_mapping_line_multiple_map():
  with pytest.raises(exceptions.ParserError):
    parser.mapping_line('a, b => c => d, e')

def test_parser_class__parse():
  content = '''
  hello, world
  bye, world
  '''
  SynParser.parse(content)

def test_parser_class__validate():
  valid = '''
  hello, world
  '''
  invalid = '''
  hello => world => world
  '''
  assert SynParser.validate(valid) is None
  with pytest.raises(exceptions.InvalidSynonyms):
    SynParser.validate(invalid)

def test_utils_load_file():
  syns = os.path.join(os.path.dirname(__file__), '../data/be-ae.synonyms')
  valid_path = os.path.abspath(syns)

  assert load_synonyms(valid_path)

def test_utils_load_incorrect_file():
  with pytest.raises(TypeError):
    load_synonyms('file://file_url_wont_work')

  with pytest.raises(TypeError):
    load_synonyms('weird_strings')

  with pytest.raises(TypeError):
    load_synonyms('./noo/nothing/here')
