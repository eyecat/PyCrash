#!/usr/bin/env python
# PyCrash - A Run-Time Exception Dumper for the Python programming language

# decrypt.py - A simple script which decrypts crash dump encrypted with
#	       EncryptedPyCrash class of pycrash.Encrypt module 

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

from Crypto.Cipher import ARC4
import Crypto.PublicKey
import getopt, sys, cPickle

def decrypt(filename, privkey):
	try:
		fo = open(filename, "r")
	except:
		print "Error: unknown file " + filename
		sys.exit(2)

	list = cPickle.load(fo)
	size = len(list)
	text = []
	i = 0
	for elem in list:
		i += 1
		sys.stderr.write("Decrypting...  \x1b[1;31m%d%%\x1b[0m\r" % ((i*100)/size)) 
		sys.stderr.flush()
		text.append( privkey.decrypt(elem) )

	try:
		print "" .join(text) 

	except:
		print "Broken pipe"

	fo.close()

def usage():
	USAGE_MSG = """
usage: decrypt.py -k keyfile -f filename 
Options and arguments:
-h, --help:	Prints this message and exit
-k, --key:	The file with private key generated by keygen.py tool
-f, --filename:	The file to decrypt
"""
	print USAGE_MSG

if __name__ == "__main__":
	try:
		opts, arg = getopt.getopt(sys.argv[1:], "k:f:", ["--key", "--filename"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	keyfile = None
	file = None

	for o, a in opts:
		if o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-k", "--key"):
			keyfile = a
		elif o in ("-f", "--filename"):
			file = a

	if keyfile is None or file is None:		
		usage()
		sys.exit(2)

	try:
		fo = open(keyfile, "r")
		key = cPickle.load(fo)
		fo.close()
	except:
		print "Can load key file \"" + keyfile + "\" or the file is corrupted or invalid"
		sys.exit(2)
	
	if not issubclass(key.__class__, Crypto.PublicKey.pubkey.pubkey):
		print "The file " + keyfile + " doesn't contain a valid key generated by keygen.py utility"

	try:
		decrypt(file, key)
	except KeyboardInterrupt:
		sys.stdout.flush()
		print "\n-Bye"

	sys.exit()