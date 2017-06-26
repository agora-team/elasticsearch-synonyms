import requests

from codecs import open
from requests.exceptions import MissingSchema, InvalidSchema, InvalidURL

from .parser import SynParser

def load_synonyms(path):
  try:
    r = requests.get(path)
    content = r.text
  except (MissingSchema, InvalidSchema, InvalidURL):
    try:
      with open(path, encoding='utf-8') as fp:
        content = fp.read()
    except OSError:
      raise TypeError('Invalid Path: "{0}". Ensure it is either a URL or Correct FS Path.'.format(path))

  return SynParser.get_mapping(content)
