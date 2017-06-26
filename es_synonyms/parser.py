from .exceptions import ParserError, ParserWarning, InvalidSynonyms
from .constants import OPERATORS, LEVELS
from .report import ReportMessage, validate_report

def empty_line(line):
  '''Empty lines are ignored by Solr.'''
  if len(line.strip()) == 0:
    return True

def comment_line(line):
  '''Comments start with a pound.'''
  if line.startswith(OPERATORS['comment']):
    return True

def mapping_line(line):
  '''A mapping should contain single `=>` and may contain several `,`.'''
  token_empty = lambda x: len(x.strip()) == 0
  all_tokens = []

  if OPERATORS['map'] in line:
    for l in line.split(OPERATORS['map']):
      all_tokens += l.split(OPERATORS['delimiter'])
  else:
    all_tokens = line.split(OPERATORS['delimiter'])

  if any(map(token_empty, all_tokens)):
    raise ParserError('Invalid mapping. Check for spaces, and trailing commas.')

  if OPERATORS['map'] in line:
    if not line.count(OPERATORS['map']) == 1:
      raise ParserError('Cannot define multiple mapping in single line')

    lhs, rhs = line.split(OPERATORS['map'])

    tokens_l = lhs.split(OPERATORS['delimiter'])
    tokens_r = rhs.split(OPERATORS['delimiter'])

    if not len(tokens_l) == len(tokens_r) and not len(tokens_r) == 1:
      raise ParserWarning('Unbalanced tokens in mapping')

  return True


class SynParser(object):
  '''Parse Solr Synonyms'''
  hooks = [empty_line, comment_line, mapping_line]

  @classmethod
  def parse(cls, content=None, filename=None):
    if content is not None:
      return cls.parse_lines(content.splitlines())
    elif filename is not None:
      with open(filename, 'r') as fp:
        return cls.parse_lines(fp)
    else:
      raise TypeError('Either content or filename is required')

  @classmethod
  def parse_lines(cls, lines):
    '''Parse a list of lines.'''
    reports = []
    for line_nb, line in enumerate(lines):
      response = cls.parse_line(line, line_nb)
      reports.append(response)
    return reports

  @classmethod
  def parse_line(cls, line, line_nb):
    '''Parse a single line.'''
    for hook in cls.hooks:
      try:
        resp = hook(line)
        if resp is True:
          return ReportMessage(LEVELS['ok'], 'Ok', line_nb + 1)
      except ParserWarning as e:
        return ReportMessage(LEVELS['warn'], str(e), line_nb + 1)
      except ParserError as e:
        return ReportMessage(LEVELS['error'], str(e), line_nb + 1)

    return ReportMessage(LEVELS['warn'], 'Undefined parser state', line_nb + 1)

  @classmethod
  def validate(cls, content):
    report = cls.parse(content)
    if not validate_report(report):
      raise InvalidSynonyms('The synonyms file is invalid.')

  @classmethod
  def get_mapping(cls, content):
    try:
      cls.validate(content)
    except InvalidSynonyms as e:
      raise e
    else:
      mappings = []
      for mline in content.splitlines():
        l = mline.strip()
        if len(l) and not l.startswith(OPERATORS['comment']):
          mappings.append(l)
      return mappings
