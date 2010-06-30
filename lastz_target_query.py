#! /bin/python
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
import os
import sys
import subprocess
from string import Template

# Data parameters.
targetdir = "/home/directory/data/monodelphis/total"
querydir = "/home/directory/data/reference/tammar12_split"
odir = "/home/directory/data/maps/tammar_mono"
tdir = "/scratch"

# Script parameters.
sdir = "./script_lastz_tammar_mono"
ldir = "./log_lastz_tammar_mono"

# Other parameters.
prog = "lastz"
sub = "/home/directory/bsub_scripts/sub.sh"
lastz = "/home/directory/opt/lastz-distrib/bin/lastz"

# Make script and log directories.
subprocess.call(["rm","-rf",sdir])
subprocess.call(["rm","-rf",ldir])
subprocess.call(["mkdir",ldir])
subprocess.call(["mkdir",sdir])

# Get list of reference.
targets = []
for f in os.listdir(targetdir):
	name = "%s/%s" % (targetdir, f)
	targets.append(name)
	

# Get list of query.
queries = []
for f in os.listdir(querydir):
	name = "%s/%s" % (querydir, f)
	queries.append(name)
	
# Build list of commands.
cmds = []
for target in targets:
	
	# build target base name.
	tbasen = os.path.basename(target).split(".")[0]
	
	for query in queries:
		
		# Build query base name.
		qbasen = os.path.basename(query).split(".")[0]
		
		# Setup other files.
		tfile = "%s/%s_%s.tmp" % (tdir, tbasen, qbasen)
		ofile = "%s/%s_%s.sam" % (odir, tbasen, qbasen)
		sfile = "%s/%s_%s.sh" % (sdir, tbasen, qbasen)
		lfile = "%s/%s_%s.log" % (ldir, tbasen, qbasen)
		
		# Make command.
        cmd = []
        cmd.append(lastz)
        cmd.append("%s[unmask,multiple]" % target)
        cmd.append("%s[unmask,multiple]" % query)
        cmd.append("--step=10")
        cmd.append("--seed=match12")
        #cmd.append("--notransition")
        #cmd.append("--exact")
        cmd.append("--nogapped")
        cmd.append("--identity=95")
        cmd.append("--coverage=90")
        cmd.append("--format=sam-")
        cmd.append(">")
        cmd.append(tfile)
        tmp_cmd = ' '.join(cmd)
        cmds.append( [tmp_cmd, ofile, sfile, lfile, tfile] )
		
# Execute each job in its own node.
for cmd in cmds:
	# Define script variables.
	cmd_txt = cmd[0]
	ofile = cmd[1]
	sfile = cmd[2]
	lfile = cmd[3]
	tfile = cmd[4]
	
	
	# Write shell script head.
	txt = """#!/bin/bash
#BSUB -J lastz
#BSUB -q normal
#BSUB -o $lfile

# Make tmprdir.
if [ -d "${tdir}" ]; then true
else
mkdir $tdir
fi
rm -f $tfile

# Execute search.
$cmd_txt

# Move out of scracth space.
mv $tfile $ofile

exit;
"""
	txt = Template(txt)
	txt = txt.substitute(lfile=lfile, tdir=tdir, tfile=tfile, cmd_txt=cmd_txt, ofile=ofile)

	sout = open(sfile, "w")
	sout.write(txt)
	sout.close()
	
	subprocess.call(["chmod","u+x",sfile])
	
# Submit scripts.
for sfile in os.listdir(sdir):
	subprocess.call([sub,"%s/%s" % (sdir, sfile)])

	

	

