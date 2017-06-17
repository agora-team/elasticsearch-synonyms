from .exceptions import ParserError, ParserWarning
from .constants import OPERATORS, LEVELS
from .report import ReportMessage

def empty_line(line):
  if len(line.strip()) == 0:
    return True

def comment_line(line):
  if line.startswith('#'):
    return True

def mapping_line(line):
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
  hooks = [empty_line, comment_line, mapping_line]

  def parse(self, content=None, filename=None):
    if content is not None:
      return self.parse_lines(content.splitlines())
    elif filename is not None:
      with open(filename, 'r') as fp:
        return self.parse_lines(fp)
    else:
      raise TypeError('Either content or filename is required')

  def parse_lines(self, lines):
    reports = []
    for line_nb, line in enumerate(lines):
      response = self.parse_line(line, line_nb)
      reports.append(response)
    return reports

  def parse_line(self, line, line_nb):
    for hook in self.hooks:
      try:
        resp = hook(line)
        if resp is True:
          return ReportMessage(LEVELS['ok'], 'Ok', line_nb + 1)
      except ParserWarning as e:
        return ReportMessage(LEVELS['warn'], str(e), line_nb + 1)
      except ParserError as e:
        return ReportMessage(LEVELS['error'], str(e), line_nb + 1)

    return ReportMessage(LEVELS['warn'], 'Undefined parser state', line_nb + 1)
