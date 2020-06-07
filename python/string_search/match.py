""" match.py Match with One Asterisk
"""
def match(text, keyword, algorithm="builtin"):
  """match. matching keyword in text. The implementation string matching algorithm with modification. 
  Some of string matching algorithm:
    1. "builtin" python string matching. It uses mix algorithm between Boyer-Moore and Horspool algorithms.
    2. "naive" simple Brute force algorithm by checking each character combination, one by one.
    3. (NotImplemented) "kmp" Knuth-Morris-Pratt algorithm

  Args:
      text (str): text where we search the regex pattern
      keyword (str): regex pattern, with limitation, we only support one asterisk
      algorithm (str): Valid value are: builtin, kmp, and naive

  Return:
    Return the index where the keyword is found in text.
  """

  validate_text_pattern(text, keyword)

  algorithm_dict = {
    "builtin" : builtin_match,
    "naive": naive_match,
    "kmp": kmp_match
  }
  matcher = algorithm_dict[algorithm]

  #handle matching without asterisk (*)
  if "*" in keyword:
    if len(keyword) > 0:
      segment_1, segment_2 = keyword.split("*")
    else:
      return 0
  else:
      return matcher(text, keyword)

  if segment_1:
    index_1 = matcher(text, segment_1)
    if index_1 != -1 :
      begin_from = index_1 + len(segment_1)
      index_2 = matcher(text, segment_2, begin=begin_from)

      #handle matching with asterisk (*) in the middle and in the end of text
      if index_2 != -1 :
        result = index_1
      else:
        result = -1
    else:
      result = -1
  else:
    index_2 = matcher(text, segment_2)
    #handle matching with asterisk (*) in beginning of text
    #it will always return 0 if the pattern after asterisk is matched
    if index_2 != -1 :
      result = 0
    else:
      result = -1
  
  return result
 
def builtin_match(text, pattern, begin=0 ):
  """builtin_match Substring matching using builtin string find method
  It uses mix algorithm between Boyer-Moore and Horspool algorithms.

  Args:
      string (str): a text to search the pattern
      pattern (str): pattern to match, it doesn't support any wildcard.
      begin (int, optional): The begining fo string index to match. Defaults to 0. 

  Return:
    int: Return the index of first matching string. Return -1 if pattern is not found.
  """
  return text.find(pattern, begin)

def naive_match(text, pattern, begin=0 ):
  """naive_match Substring matching using naive algorithm

  Args:
      string (str): a text to search the pattern
      pattern (str): pattern to match, it doesn't support any wildcard.
      begin (int, optional): The begining fo string index to match. Defaults to 0. 

  Return:
    int: Return the index of first matching string. Return -1 if pattern is not found.
  """
  text = text[begin:]
  len_text = len(text) 
  len_pattern = len(pattern)

  if len_pattern == 0:
    return 0

  if len_text < len_pattern:
    return -1

  for ii in range(len_text - len_pattern + 1): 
    jj = 0  

    for jj in range(0, len_pattern): 
      if (text[ii + jj] != pattern[jj]): 
        break
      if (jj == len_pattern - 1):
        return ii + begin

  return -1

def kmp_match(text, pattern, begin=0):
  """kmp_match Knuth-Morris-Pratt algorithm string matching
    Currently, it is not implemented. This function just illustrate the algorithm can be expanded.

  Args:
      string (str): a text to search the pattern
      pattern (str): pattern to match, it doesn't support any wildcard.
      begin (int, optional): The begining fo string index to match. Defaults to 0. 

  Return:
    int: Return the index of first matching string. Return -1 if pattern is not found.

  """
  return NotImplemented

def validate_text_pattern(text, keyword):
  """validate_input [summary]

  Args:
      text (str): text where we search the regex pattern
      keyword (str): regex pattern, with limitation, we only support one asterisk

  """
  if not isinstance(text, str):
    raise TypeError("text must be a string")

  if not isinstance(keyword, str):
    raise TypeError("pattern must be a string")

  if keyword.count("*") > 1:
    raise ValueError("keyword/pattern only support a single asterisk")


import unittest
def run_tests(test_class):
  suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
  runner = unittest.TextTestRunner(verbosity=2)
  result = runner.run(suite)

class TestMatch(unittest.TestCase):

  def test_example1(self):
    self.assertEqual(0, match("eggprata", "e*prat"))
    self.assertEqual(0, match("eggprata", "e*prat", algorithm='naive'))

  def test_example2(self):
    self.assertEqual(3, match("eggprata", "pra*t"))
    self.assertEqual(3, match("eggprata", "pra*t", algorithm='naive'))

  def test_example3(self):
    self.assertEqual(-1, match("eggprata", "haha*haha"))
    self.assertEqual(-1, match("eggprata", "haha*haha", algorithm='naive'))

# run_tests(TestMatch)

from sys import argv
if __name__ == '__main__':
  try:
    text = argv[1]
    keyword = argv[2]
  except IndexError:
    print('usage: python3 match.py TEXT KEYWORD')
    exit()

  print(f'Searching for "{keyword}" in "{text}".')
  match_result = match(text, keyword)
  print(f"Result: {match_result}")

