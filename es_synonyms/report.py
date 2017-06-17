import hues
import collections

from .constants import LEVELS


ReportMessage = collections.namedtuple('ReportMessage', ['level', 'msg', 'line_nb'])


def print_reports(reports, verbose=False):
  errored = False
  for report in reports:
    if report.level == LEVELS['ok']:
      if verbose:
        hues.log(report.line_nb, report.msg, time=False)
      continue
    elif report.level == LEVELS['warn']:
      hues.log(report.line_nb, report.msg, time=False, warn=True)
    elif report.level == LEVELS['error']:
      hues.log(report.line_nb, report.msg, time=False, error=True)
      errored = True
  if not errored:
    hues.log('Valid Synonyms', time=False, success=True)
  return errored
