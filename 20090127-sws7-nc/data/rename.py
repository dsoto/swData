#!/usr/bin/python
# meant to rename a list of files based on strings in the filename
# daniel soto
# Tue Dec 11 02:58:17 PST 2007

# hack solution using two redundant loops
# seems better if you could have a dictionary of strings and replacements
# and then you went through the dictionary during the loop

import re
import os

regString = 'txt'
regExp = re.compile(regString)

for fname in os.listdir(os.getcwd()):
	print fname,
	foutName = regExp.sub('data',fname)
	print foutName
#	os.rename(fname, foutName)
	command = "git mv " + fname + " " + foutName
	print command
	os.system(command)