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

import types
import hashlib
from stackframe import StackFrame
from xml.sax.saxutils import escape

_TupleType = types.TupleType
_TracebackType = types.TracebackType
_StringType = types.StringType
del types

class ExceptionTraceBack(object):
	
	__initialized = 0
	
	def __init__(self, thread, traceback):
		assert type(thread) is _StringType and len(thread) > 0, "2nd parameter must be an unique string identifier"
		assert type(traceback) is _TupleType and type(traceback[2]) is _TracebackType, "use sys.exc_info() to retrieve 3rd parameter"

		self.__tb = traceback[2]
		self.__excInfo = [traceback[0], traceback[1]]
		self.__thread = thread
		self.__stack = []
		self.__initialized = 1

		self.__parseTraceBack()

	def __parseTraceBack(self):
		tb = self.__tb

		while tb is not None:
			self.__stack.append(StackFrame(tb.tb_frame))
			tb = tb.tb_next

		self.__stack.reverse() #We reverse list so last called routine is
				      #the first one

	def getStack(self):
		return self.__stack

	def toXML(self):
		strXML = "\t<exctb thread=\""
		strXML += escape(str(self.__thread))
		strXML += "\" exctype=\"" + escape(str(self.__excInfo[0])) 
		strXML += "\" value=\"" + escape(str(self.__excInfo[1])) + "\">\n"

		for stack in self.__stack:
			strXML += stack.toXML()

		strXML += "\t</exctb>\n"

		return strXML
	def getLocationTrace(self):
		return ["%s:%d"%(f.getFileName(),f.getLineNumber()) for f in self.__stack]
	def getTBHash(self):
		m = hashlib.md5()
		m.update(str(self.__excInfo[0]))
		m.update(str(self.__excInfo[1])[:20])#ODBC driver will include too much variable details in exception value.
		for f in self.__stack:
			m.update('\n')
			m.update(f.getFileName())
			m.update(':')
			m.update(f.getLineNumber())
		return m.hexdigest()
		
