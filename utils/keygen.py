#!/usr/bin/env python
# PyCrash - A Run-Time Exception Dumper for the Python programming language

# keygen.py - A public/private keys generator to use in conjunction with 
#	      PyCrash module. 

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

from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
import pickle, getopt, sys, math

def generate(bits, filename):
	rp = RandomPool()
	key = RSA.generate(bits, rp.get_bytes)
	public_key = key.publickey()
	public_dump = pickle.dumps(public_key)
	private_dump = pickle.dumps(key)

	try:
		fo = open(filename + ".priv", "w")
		fo.write(private_dump)
		fo.close
		
		fo = open(filename + ".pub", "w")
		fo.write(public_dump)
		fo.close
	except IOError, msg:
		print msg
		sys.exit(2)
	else:
		print "Your private key stored in \x1b[1;31m" + filename + ".priv\x1b[0m file. Keep it safe"
		print "Your public key stored in \x1b[1;31m" + filename + ".pub\x1b[0m file. This is the key you can freely distribute with your applications"

def usage():
	USAGE_MSG = """
usage: keygen.py [options]
Options and arguments:
-h, --help:	Prints this message and exit
-b, --bits: 	Specify how many bits to use to generate public/private keys
-f, --filename: Specify the file name prefix where public and private keys will be stored
"""
	print USAGE_MSG

if __name__ == "__main__":
	try:
		opts, arg = getopt.getopt(sys.argv[1:], "hb:f:", ["help", "bits", "filename"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	bits = 512
	filename = "key"
	
	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-b", "--bits"):
			bits = int(a)
			if bits < 512:
				print "Error: a key must be >= 512 bits"
				sys.exit(2)
			else:
				bits = int(a)
				exp = math.modf(math.log(bits, 2))
				if exp[0] != 0.0:
					print "Error: a key must be of type 2^x"
					sys.exit(2)

		elif o in ("-f", "--filename"):
			filename = a

	generate(bits, filename)
	sys.exit()
