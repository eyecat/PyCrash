#!/usr/bin/env python
# PyCrash - A Run-Time Exception Dumper for the Python programming language

# pycrash2html.py - A simple converter from PyCrash XML dump to HTML format

# (C)Copyright Carmine Ivan Delio Noviello 2003-2004 <cnoviello@pycrash.org>
#
# For further informations, please refer to: www.pycrash.org
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from pycrash.utils.Html import HTMLPyCrash
import getopt, sys

def usage():
	USAGE_MSG = """
usage: pycrash2html.py -f filename [OPTIONS]
Options and arguments:
-c, --css: Specify a custom CSS
-f, --filename:	The file to decrypt
-h, --help:	Prints this message and exit
-i, --hide:	Hide[1]/Show[0] images in dump
"""
	print USAGE_MSG

class DumpConverter(HTMLPyCrash):
	def __init__(self):
		HTMLPyCrash.__init__(self, {"":""})

	def getInfoText(self):
		return ""

if __name__ == "__main__":
	try:
		opts, arg = getopt.getopt(sys.argv[1:], "i:f:c:", ["--hide", "--filename", "--css"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	hide = None
	file = None
	css = None

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-i", "--hide"):
			if a == "1" or a == "0":
				hide = a
			else:
				print "Bad paramtere: use '-i 0' to hide or '-i 1' to show imageas"
				sys.exit(2)
		elif o in ("-f", "--filename"):
			file = a
		elif o in ("-c", "--css"):
			css = a

	if file is None:		
		usage()
		sys.exit(2)

	try:
		p = DumpConverter() 
		if hide is not None:
			p.hideImages(int(hide))
		if css is not None:
			p.setCSS(css)

		htmlDump = p.convertFileDump(file)

		try: #let's store dump in a new file
			fo = open(file + ".html", "w+")
			fo.write(htmlDump)
			fo.close()
		except IOError:
			print "Error in writing output file"

	except KeyboardInterrupt:
		sys.stdout.flush()
		print "\n-Bye"

	sys.exit()
