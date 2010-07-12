#!/bin/python
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
# Preps Repeat Masker for execution on cluster.
import sys
import os
import subprocess
from string import Template

# Manually define folders of interest.
appbase = "/home/jlindsay/repeat_masker_deploy"
indir = "%s/data/input" % appbase
outdir = "%s/data/output" % appbase

sdir = "%s/scripts" % appbase
ldir = "%s/logs" % appbase
tdir = "/scratch/jlindsay"

# Program locations.
sub = "/home/jlindsay/MyBin/sub_lsf.sh"
rmasker = "/home/jlindsay/repeat_masker_deploy/software/RepeatMasker/RepeatMasker"

# Check for split reference.
lls = os.listdir(indir)
if len(lls) < 2:
	print "Need to split reference up."
	sys.exit()

# Clear out old files.
subprocess.call(["rm","-rf", sdir])
subprocess.call(["rm","-rf", ldir])
subprocess.call(["rm","-rf", outdir])

subprocess.call(["mkdir", sdir])
subprocess.call(["mkdir", ldir])
subprocess.call(["mkdir", outdir])

# Create each instance.
for infile in lls:

	# Get base.
	basen = infile.split(".")[0]
	fullin = "%s/%s" % (indir, infile)

	# Create script and log files.
	sfile = "%s/%s.sh" % (sdir,basen)
	lfile = "%s/%s.log" % (ldir,basen)
	
	# Create final output directory.
	outfolder = "%s/%s" % (outdir,basen)
	
	# Create temporary files needed.
	otemp = "%s/%s.out.tmp" % (tdir, basen)
	itemp = "%s/%s" % (tdir, infile)
	
	# Create repeat masker command.
	cmd_txt = "%s -e crossmatch -gff -dir %s %s" % (rmasker, otemp, itemp)
	
	txt = """#!/bin/bash
#BSUB -J repmask
#BSUB -q normal
#BSUB -o $lfile

# Make tmprdir.
if [ -d "${tdir}" ]; then true
else
mkdir $tdir
fi

# Remove output dir if present.
rm -rf $otemp

# Copy file to local.
cp $fullin $itemp

# Swtich to tmp dir.
cd $tdir

# Execute search.
$cmd_txt

# Move out of scratch space.
mv $otemp $outfolder

exit;
"""
	txt = Template(txt)
	txt = txt.substitute(lfile=lfile, tdir=tdir, fullin=fullin, itemp=itemp, otemp=otemp, cmd_txt=cmd_txt, outfolder=outfolder)
	
	# Write script.
	sout = open(sfile,"w")
	sout.write(txt)
	sout.close()
	
	# Make execuateble.
	subprocess.call(["chmod","u+x",sfile])
	
# Submit scripts.
for sfile in os.listdir(sdir):
	fpath = "%s/%s" % (sdir, sfile)
	subprocess.call([sub,fpath])
