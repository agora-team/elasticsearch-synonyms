import argparse
import sys
import hues

from .parser import SynParser
from .report import print_reports


def cli():
  parser = SynParser()
  cli = argparse.ArgumentParser(description='Parse and validate Solr Synonyms file.')
  cli.add_argument('file', help='Solr Synonyms file', nargs='+')
  cli.add_argument('-v', '--verbose', action='store_true', help='Print a verbose report')

  args = cli.parse_args()

  status = 0
  for fname in args.file:
    hues.info('Validating', fname)
    reports = parser.parse(filename=fname)
    error = print_reports(reports, args.verbose)
    if error:
      status += 1

  sys.exit(status)
