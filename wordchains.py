#!/usr/bin/env python3

"""
Author: Johannes Degn <j@degn.de>
 This script uses the recursive function mutation in order to find the end value
 starting with a start value
"""

import argparse
import sys



def main():
  usage = "usage: wordchains [-d <dictionary file>] [--create-hash]"
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument("-d", "--dictionary", help="Dictionary file to use, defaults to /usr/share/dict/words", default="/usr/share/dict/words", nargs='?')
  parser.add_argument("-c", "--create-hash", help="create a hashmap of whole dictionary. This might take a while.", default=False, action="store_const", const=True)
  global options
  options = parser.parse_args().__dict__
# load dictionary in set
  dict_file = open(options['dictionary'], 'r')
  global dictionary
  dictionary = set(dict_file.read().lower().split())
  print('dictionary file loaded: %d  entries' % len(dictionary)) 
 
  if options['create_hash']: # hash all mutations in a big hash map
    print ('creating hash (this might take a while for big dictionaries')
    entries = len(dictionary)
    global hash_map
    hash_map = {}
    counter = 0
    for word in dictionary:
      counter += 1
      sys.stdout.write('%.2f%% done\r' % (counter/entries*100))
      hash_map[word] = getmutations(word, hashing = True)
  while True:
    print('waiting for input...')
    r = sys.stdin.readline().lower()
    if r in ['exit\n', 'quit\n', 'stop\n', 'let me out\n']:
      break

    r = r.split()
    if (len(r) % 2 != 0) or (len(r) == 0): # we need at least one start and one end value
      print ('\nexpected input: <startword> <endword> [<startword2> <endword2> ...] \n please enter pairs of words')
      continue

    # we have received at least one pair of words

    while r:
      end, start = r.pop(), r.pop()
      print ('searching word chain from %s to %s' % (start, end))
      result = wordchain(start, end, [])
      if (result):
        print ('YES')
        print ('%s and %s are connected' % (start, end))
      else:
        print ('NO')
        print ('%s and %s are not connected' % (start, end))

def wordchain(startvalue, endvalue, checked = []):
  mutations = getmutations(startvalue)
  checked.append(startvalue)
  if ismutation(startvalue, endvalue) or endvalue in mutations:  # we found the endvalue
    checked.append(endvalue)
    return checked
  else:
    for new_start in mutations:   
      if not new_start in checked: # make sure we dont double check words
        return wordchain(new_start, endvalue, checked)

def getmutations(word, hashing = False):  # checks dictionary for permutations of word
  if (not hashing) and options['create_hash']:
    if word in hash_map.keys():
      return hash_map[word]
  
  mutations = set()
  for dict_word in dictionary:
    if ismutation(word, dict_word):
      mutations.add(dict_word)
  #print ('mutations of %s: %s\n\n\n' % (word, mutations)) 
  return mutations

def ismutation(word1, word2):
  if word1 == word2: # probably not best to put if here...
    return False
  diff = abs(len(word1)-len(word2)) 
  if diff > 1:  
    return False  # shortcut
  elif diff == 1:
    if not letterdeleted(word1, word2):
      return False
  elif diff == 0: # if size is the same
    diff += check_letters(word1, word2)
  else:
    return False
  return diff < 2 

def check_letters(word1, word2): # hamming distance, word1 and word2 need to be of same length
  diff = 0
  return sum(letter1!=letter2 for letter1, letter2 in zip(word1, word2))

def letterdeleted(word1, word2):
  if len(word2) > len(word1):
    word2, word1 = word1, word2
  for pos,letter in enumerate(word1):
    temp = ''.join([word1[:pos], word1[pos+1:]]) # join is faster than concatenate and we check for deleted letters a lot
    if temp == word2:
      return True
  return False

if __name__ == "__main__":
  main()
