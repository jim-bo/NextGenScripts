#!/usr/bin/python
"""
 Copyright (c) <2010> <James Lindsay>

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE
 """
""" This program counts number or reads, and gives avg length """
import os
import sys

# Usage.
if len(sys.argv) < 2:
	print ""
	print "This program takes a multiple fasta file and splits it into a certain number of files."
	print "Usage: %s -in file -c number -o outbase"
	print "-in: fasta file"
	print "-c: number of files"
	print "-o: basename of output files."
	print "places files into current directory"
	print ""
	sys.exit()

# Parse args.
for i in range(len(sys.argv)):
	if sys.argv[i] == "-in":
		infile = sys.argv[i+1]
	elif sys.argv[i] == "-c":
		numfiles = int(sys.argv[i+1])
	elif sys.argv[i] == "-o":
		outbase = sys.argv[i+1]

# Setup output files.
ofiles = []
for i in range(numfiles):
	name = "%s_%i.fasta" % (outbase, i)
	ofiles.append(open(name,"w"))

# Read input files.
fin = open(infile,"r")
seq = ""
seqheader = ""
phase = 0
j = 0
for line in fin:
	# Skip comments.	
	if line[0] == "#": continue

	# check for finish with seq.
	if phase == 1 and line[0] == ">":
		# Output data.
		ofiles[j].write("%s\n" % seqheader)
		ofiles[j].write("%s\n" % seq)

		# Reset variables.
		if j == numfiles - 1: j = 0
		else: j += 1
		seq = ""
		seqheader = ""
		phase = 0


	# Get seq header.
	if phase == 0:
		seqheader = line.strip()		
		phase += 1
		continue

	# Get seq.
	if phase == 1:
		# Save sequence.
		seq += line.strip()
		continue

# Print last.
ofiles[j].write("%s\n" % seqheader)
ofiles[j].write("%s\n" % seq)

		
# Finish up
fin.close()
