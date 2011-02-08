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

import types, string

_InstanceType	= types.InstanceType
_FrameType	= types.FrameType
del types

_replace 	= string.replace
del string

class StackFrame:
	def __init__(self, frame):
		assert type(frame) is _FrameType, "1st parameter must be a Frame object"
		
		self._frame = frame

	def getArgCount(self):
		return self._frame.f_code.co_argcount

	def getFileName(self):
		filename =  self._frame.f_code.co_filename
		#replacing '<' and '>' with '(' and ')'
		#to avoid XML parser errors
		filename = _replace(filename, "<", "(")
		filename = _replace(filename, ">", ")")
		return filename
	
	def getLineNumber(self):
		# Coded by Marc-Andre Lemburg from the example of PyCode_Addr2Line()
		# in compile.c.
		# Revised version by Jim Hugunin to work with JPython too.

		c = self._frame.f_code
		if not hasattr(c, 'co_lnotab'):
			return self._frame.f_lineno
			
		tab = c.co_lnotab
		line = c.co_firstlineno
		stopat = self._frame.f_lasti
		addr = 0
		for i in range(0, len(tab), 2):
			addr = addr + ord(tab[i])
			if addr > stopat:
				break
			line = line + ord(tab[i+1])
		return line
		
	def getFrameName(self):
		return str(self._frame.f_code.co_name)

	def getStackSize(self):
		return self._frame.f_code.co_stacksize
	
	def getVar(self, name):
		assert name is not "", "1st parameter must be a string keyword"
		return self._frame.f_locals[name]

	def getVarNames(self):
		return self._frame.f_code.co_varnames

	def toXML(self):
		#frame info
		strXML = "\t\t<frame name=\"" + self.getFrameName() + "\""
		strXML += " argcount=\"" + str(self.getArgCount()) + "\""
		strXML += " size=\"" +  str(self.getStackSize()) + "\""
		strXML += " filename=\"" + self.getFileName() + "\""
		strXML += " line=\"" +  str(self.getLineNumber()) + "\">\n"

		#var info
		import re
		regex = re.compile("'[a-z]+'", re.IGNORECASE)
		
		for item in self.getVarNames():
			var = None
			try: #the variable can be undefined
				var = self.getVar(item)
				varValue = str(var)
				varType = str(type(var))
				
				#replacing '<' and '>' with '(' and ')'
				#to avoid XML parser errors
				varValue = _replace(varValue, "<", "(")
				varValue = _replace(varValue, ">", ")")
				
				#skip <type 'XX'> text
				search = regex.search(varType)
				if search is not None: 
					varType = varType[search.start() + 1:search.end() - 1]
				else:
					varType = "(undefined)"
			except:
				varValue = "(undefined)"
				varType = "(undefined)"
			
			strXML += "\t\t\t<var name=\"" + item + "\""
			strXML += " type=\"" + varType + "\">" + varValue
			
			if type(var) == _InstanceType: #Add all object attributes
				attrKeys = var.__dict__.keys()
				del attrKeys[0] #Let's skip 1st element to avoid redundant info
				for attr in attrKeys:
					varType = str(type(var.__dict__[attr]))
					search = regex.search(varType)
					if search is not None: #skip <type 'XX'> text
						varType = varType[search.start() + 1:search.end() - 1]
					else:
						varType = "(undefined)"
					strXML += "\n\t\t\t\t<attr name=\"" + attr 
					strXML += "\" type=\"" + varType + "\">"
					attrValue =  str(var.__dict__[attr])
					attrValue = _replace(attrValue, "<", "(")
					attrValue = _replace(attrValue, ">", ")")
					strXML += attrValue + "</attr>"
				strXML += "\n\t\t\t</var>\n"
			else:
				strXML += "</var>\n"
			
		strXML += "\t\t</frame>\n"
		return strXML
