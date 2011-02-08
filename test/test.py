#!/usr/bin/python

#A simple and very stupid test for PyCrash Module

from pycrash import *
from thread import *

class MyCrash(PyCrash):
	def onExit(self):
		self.saveToFile("./test.pycrash")

class Foo2:
	def pro2(self):
		pass

class Foo:
	def __init__(self):
		self.__int = 10
		self.__str = "Ciao"
		self.__instance = self
		self.proi = Foo2.pro2

	def pro(self):
		pass

def bad_func(a):
	f = Foo()
	
	if a > 0:
		bad_func(a-1)
	else:
		prova = a/0 #Error

if __name__ == '__main__':
	print "Testing PyCrash..."
	p = MyCrash({'AppName': 'Test', 'Version':'0.2', 'SendTo': 'Carmine I.D. Noviello <cnoviello@programmers.net>'})
	
	start_new_thread(bad_func, (11,))
	start_new_thread(bad_func, (100,))

	func_ref = bad_func

	bad_func(2)

	try:
		while 1:
			pass
	except KeyboardInterrupt:
		print "bye"
