import pytest

from es_synonyms import parser
from es_synonyms import exceptions

def test_parse_empty_line():
  assert parser.empty_line(' ') is True
  assert parser.empty_line('\n') is True
  assert parser.empty_line('42') is None

def test_parse_comment_line():
  assert parser.comment_line('# 42') is True
  assert parser.comment_line('42') is None

def test_parse_mapping_line():
  assert parser.mapping_line('42') is None
  assert parser.mapping_line('a => b') is True
  assert parser.mapping_line('a, b => c, d') is True
  assert parser.mapping_line('a, b => c') is True

def test_parse_mapping_line_unbalanced_tokens():
  with pytest.raises(exceptions.ParserWarning):
    parser.mapping_line('a, b => c, d, e')

def test_parse_mapping_line_multiple_map():
  with pytest.raises(exceptions.ParserError):
    parser.mapping_line('a, b => c => d, e')
