#!/bin/python3 
import os

foo='/home/bgirton-local/.roxanne/firefox/professor.txt'

def getAbsentParents(inpath):
   curpath = inpath
   result = False
   output = []
   while not result:
      curpath = os.path.dirname(curpath)
      if not os.path.isdir(curpath):
         output.append(curpath)
      else:
         result = True
   return sorted(output)

alpha = getAbsentParents(foo)

for thisdir in alpha:
   print ('need to mkdir ', thisdir)
