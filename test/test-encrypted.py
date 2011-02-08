# PyCrash - A Run-Time Exception Dumper for the Python programming language
#
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

#!/usr/bin/python

#A simple and very stupid test for EncryptedPyCrash and PyCrash module

from pycrash import *
from pycrash.utils.Encrypt import EncryptedPyCrash
from thread import *
import sys

class MyEncryptedCrash(EncryptedPyCrash):
	def encryptingProgress(self, percentage):
		print "Encrypting...  \x1b[1;31m%d%%\x1b[0m\r" % percentage, 
		sys.stdout.flush()

	def onExit(self):
		try:
			self.setPubKeyFilename("./key.pub")
		except:
			print "Run keygen.py before to use this program"
		else:
			self.saveToFile("./test.pycrash.encrypted")

class Foo:
	def __init__(self):
		self.__int = 10
		self.__str = "Hello"
		self.__instance = self

	def aFooMethod(self):
		pass

def bad_func(a):
	f = Foo()
	
	if a > 0:
		bad_func(a-1)
	else:
		prova = a/0 #Error

if __name__ == '__main__':
	print "Testing EncryptedPyCrash..."
	p = MyEncryptedCrash({'AppName': 'Test-Encrypted', 'Version':'0.4pre2', 'SendTo': 'Carmine I.D. Noviello <cnoviello@pycrash.org>'})
	p.enable() #New in PyCrash-0.4pre2

	start_new_thread(bad_func, (10,))
	start_new_thread(bad_func, (10,))

	func_ref = bad_func

	func_ref(2)

	try:
		while 1:
			pass
	except KeyboardInterrupt:
		print "-Bye"
