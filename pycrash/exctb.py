# PyCrash - A crash handler for the Python programming language
#
# (C)Copyright Carmine Ivan Delio Noviello 2003 <cnoviello@programmers.net>
#
# For further informations, please refer to: pycrash.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import types
from stackframe import StackFrame

_TupleType = types.TupleType
_TracebackType = types.TracebackType
_StringType = types.StringType
del types

class ExceptionTraceBack:
	
	__initialized = 0
	
	def __init__(self, thread, traceback):
		assert type(thread) is _StringType and len(thread) > 0, "2nd parameter must be an unique string identifier"
		assert type(traceback) is _TupleType and type(traceback[2]) is _TracebackType, "use sys.exc_info() to retrieve 3rd parameter"

		self._tb = traceback[2]
		self._excInfo = [traceback[0], traceback[1]]
		self._thread = thread
		self._stack = []
		self.__initialized = 1

		self.__parseTraceBack()

	def __parseTraceBack(self):
		tb = self._tb

		while tb is not None:
			self._stack.append(StackFrame(tb.tb_frame))
			tb = tb.tb_next

		self._stack.reverse() #We reverse list so last called routine is
				      #the first one

	def getStack(self):
		return self._stack

	def toXML(self):
		strXML = "\t<exctb thread=\""
		strXML += str(self._thread)
		strXML += "\" exctype=\"" + str(self._excInfo[0]) 
		strXML += "\" value=\"" + str(self._excInfo[1]) + "\">\n"

		for stack in self._stack:
			strXML += stack.toXML()

		strXML += "\t</exctb>\n"

		return strXML
