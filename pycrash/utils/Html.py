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

import pycrash
from xml.dom.minidom import parseString, parse
from xml.parsers.expat import ExpatError
import string, time

_strftime = time.strftime
del time

_parseString = parseString
_parse = parse
del parseString, parse

_strip = string.strip
del string

IMAGE_VAR_INT = "http://pycrash.sf.net/htmldump/images/intvar.gif"
IMAGE_VAR_STRING = "http://pycrash.sf.net/htmldump/images/stringvar.gif"
IMAGE_VAR_UNDEFINED = "http://pycrash.sf.net/htmldump/images/undefvar.gif"
IMAGE_VAR_INSTANCE = "http://pycrash.sf.net/htmldump/images/instancevar.gif"
IMAGE_VAR_FUNCTION = "http://pycrash.sf.net/htmldump/images/funcvar.gif"
IMAGE_VAR_TYPE = "http://pycrash.sf.net/htmldump/images/typevar.gif"
IMAGE_VAR_LIST = "http://pycrash.sf.net/htmldump/images/listvar.gif"
IMAGE_VAR_MODULE = "http://pycrash.sf.net/htmldump/images/modulevar.gif"


IMAGE_DICTIONARY = {"(undefined)": IMAGE_VAR_UNDEFINED,
					"int": IMAGE_VAR_INT,
					"str": IMAGE_VAR_STRING,
					"instance": IMAGE_VAR_INSTANCE,
					"function": IMAGE_VAR_FUNCTION,
					"builtin_function_or_method": IMAGE_VAR_FUNCTION,
					"type": IMAGE_VAR_TYPE,
					"classobj": IMAGE_VAR_TYPE,
					"list": IMAGE_VAR_LIST,
					"module": IMAGE_VAR_MODULE }

class ExcTb:
	def __init__(self, domnode, index):
		assert domnode is not None, "1st parameter must by a DOM node object"

		self.__domNode = domnode
		self.__stackFrameList = []

		i = 0
		for node in domnode.getElementsByTagName("frame"):
			self.__stackFrameList.append(StackFrame(node, i))
			i += 1

	def getExcType(self):
		return self.__domNode.getAttribute("exctype")
		
	def getExcValue(self):
		return self.__domNode.getAttribute("value")
		
	def getStackFrameList(self):
		return self.__stackFrameList
	
	def getThreadName(self):
		return self.__domNode.getAttribute("thread")

	def toHTML(self):
		html = "<div class=\"exctb\">\n"
		html += "\t<div class=\"excinfo\">\n"
		html += ("\t\t<b>Thread Name</b>: <span class=\"data\">%s</span><br />\n" % self.getThreadName())
		html += ("\t\t<b>Exception Type</b>: <span class=\"data\">%s</span><br />\n" % self.getExcType())
		html += ("\t\t<b>Exception Value</b>: <span class=\"data\"><b>%s</b></span>\n" % self.getExcValue())
		html += "\t</div><!-- excinfo -->\n"
		html += "\t<div class=\"framelist\">"

		for frame in self.__stackFrameList:
			html += frame.toHTML()
			html += "<br />"
	
		html += "</div><!-- framelist -->"
		html += "</div><!--exctb -->"

		return html
 

class StackFrame:
	def __init__(self, domnode, index):
		assert domnode is not None, "1st parameter must by a DOM node object"

		self.__domNode = domnode
		self.__index = index
		self.__varList = None
	
	def getArgCount(self): #Returns number of parameters
		return int(self.__domNode.getAttribute("argcount"))

	def getIndex(self):
		return self.__index

	def getFileName(self):
		return self.__domNode.getAttribute("filename")

	def getFrameName(self):
		return self.__domNode.getAttribute("name")

	def getLineNumber(self):
		return int(self.__domNode.getAttribute("line"))

	def getFrameSize(self):
		return self.__domNode.getAttribute("size")

	def getVarList(self):
		#To prevent memory leak, each varList is intizialized at first use
		if self.__varList is None:
			self.__varList = []
			i = 0
			for node in self.__domNode.getElementsByTagName("var"):
				if i < self.getArgCount():
					self.__varList.append(Var(node, i, 1))
				else:
					self.__varList.append(Var(node, i))
				i += 1
		return self.__varList

	def toHTML(self):
		html = "<div class=\"stackframe\">\n"
		html += "\t<div class=\"stackframeinfo\">\n"
		html += "\t<table>\n\t<tr>\n"
		html += ("\t\t<td><b>Frame Name</b>: <span class=\"data\"><b>%s</b></span></td>\n" % self.getFrameName())
		html += ("\t\t<td><b>Frame Size</b>: <span class=\"data\">%s</span></td>\n" % self.getFrameSize())
		html += "\t</tr>\n\t<tr>\n"
		html += ("\t\t<td><b>File Name</b>: <span class=\"data\">%s</span></td>\n" % self.getFileName())
		html += ("\t\t<td><b>Line Number</b>: <span class=\"data\">%s</span></td>\n" % self.getLineNumber())
		html += "\t</tr>\n\t</table>"
		html += "\t</div><!-- stackframeinfo -->\n"

		html += "\t<div class=\"varlist\">\n"
		html += "\t\t<table cellspacing=\"0\" cellpadding=\"1px\" width=\"100%\">\n\t\t<tr class=\"firstrow\">"
		html += "\t\t\t<td><b>Variable Name</b></td><td><b>Variable Type</b></td><td><b>Variable Value</b></td><td><b>Is a parameter</b></td>\n"
		html += "\t\t</tr>\n"

		i = 0
		for var in self.getVarList():
			if i:
				i = 0
				html +="\t\t<tr style=\"background:#f7eee1\">\n"
			else:
				i = 1
				html +="\t\t<tr>\n"
			html += var.toHTML()

		html += "\t\t</table>"
		html += "\t</div><!-- varlist -->\n"
		html += "</div><!-- stackframe -->"
		return html

class Var:
	def __init__(self, domnode, index, parameter=0):
		assert domnode is not None, "1st parameter must by a DOM node object"

		self.__domNode = domnode
		self.__index = index
		self.__isParameter = parameter
		self.__attrList = None

	def __getText(self, nodelist):
		rc = ""
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc += node.data

		return _strip(rc) 

	def isParameter(self):
		return self.__isParameter

	def getAttrList(self):
		self.__attrList = []
		i = 0
		try:
			for node in self.__domNode.getElementsByTagName("attr"):
				self.__attrList.append(Var(node, None, i))
		except:
			pass
		return self.__attrList

	def getAttrList2(self):
		if self.getVarType() == "instance" and self.__attrList is None:
			self.__attrList = []
			i = 0
			for node in self.__domNode.getElementsByTagName("attr"):
				self.__attrList.append(Var(node, None, i))

		return self.__attrList

	def getStackFrame(self): #Returns reference to Stack Frame object
		return self.__stackFrameRef

	def getVarName(self):
		return self.__domNode.getAttribute("name")

	def getVarType(self):
		return self.__domNode.getAttribute("type")

	def getVarValue(self):
		return self.__getText(self.__domNode.childNodes)
		
	def getIndex(self):
		return self.__index

	def toHTML(self):
		def getImage(var):
			try:
				return IMAGE_DICTIONARY[var.getVarType()]
			except:
				if len(var.getAttrList()) > 0: #Ok, this is a new-style object, because it is an
											   #user defined type and has attributes 
					return IMAGE_VAR_INSTANCE
				else: #It's an unknown type for PyCrash
					return IMAGE_VAR_UNDEFINED

		html = ("\t\t\t<td><img alt=\"img\" src=\"%s\" />" % getImage(self) )
		html += ("<span class=\"data\">%s</span></td>\n" % self.getVarName() ) 
		html += ("\t\t\t<td><span class=\"data\">%s</span></td>\n" % self.getVarType())
		html += ("\t\t\t<td><span class=\"data\">%s</span></td>\n" % self.getVarValue())
		if self.isParameter():
			param = "Yes"
		else:
			param = "No"
		html += ("\t\t\t<td><span class=\"data\">%s</span></td>\n" % param)
		html += "\t\t</tr>\n"
		
		attrs =  self.getAttrList()
		if len(attrs) > 0:
			for attr in attrs:
				html += "\t\t<tr style=\"background:#d8d8d8\">\n"
				html += ("\t\t\t<td>&nbsp;&nbsp;&nbsp;&nbsp;<img alt=\"img\" src=\"%s\" />" % getImage(attr) )
				html += ("<span class=\"data\">%s</span></td>\n" % attr.getVarName() ) 
				html += ("\t\t\t<td><span class=\"data\">%s</span></td>\n" % attr.getVarType())
				html += ("\t\t\t<td><span class=\"data\">%s</span></td>\n" % attr.getVarValue())
				html += "\t\t\t<td><span class=\"data\">No</span></td>\n"
				html += "\t\t</tr>\n"
				
		return html

class AppData:
	def __init__(self, dom):
		assert dom is not None, "1st parameter must by a DOM object"

		self.__dom = dom
		self.__excTbList = []
		self.__customRecords = []

		#Build Exception Traceback list
		i = 0
		for node in dom.getElementsByTagName("exctb"):
			self.__excTbList.append(ExcTb(node, i))
			i += 1
		
	def __getText(self, nodelist):
		rc = ""
		for node in nodelist:
			if node.nodeType == node.TEXT_NODE:
				rc += node.data

		return _strip(rc) 

	def getAppName(self):
		return self.__dom.getAttribute("appname")

	def getAppVersion(self):
		return self.__dom.getAttribute("appversion")

	def getCustomRecords(self):
		if len(self.__customRecords) == 0:
			for node in self.__dom.getElementsByTagName("customrecord"):
				self.__customRecords.append(self.__getText(node.childNodes))

		return self.__customRecords

	def getExcTbList(self):
		return self.__excTbList

	def getOsInfo(self):
		#PyCrash uses 'os.uname()' to retrieve OS info. This function is only
		#available for UNIX-like system. So, getOsInfo() can give the
		#"(unknown)" value if the crash dump coming from other OSs (eg. Windows)
		if self.__dom.getAttribute("osinfo") != "(unknown)":			
			osinfo = eval(self.__dom.getAttribute("osinfo"))
		else:
			osinfo = []
			for i in range(5):
				osinfo.append("(unknown)")

		return osinfo	
	
	def getPythonVersion(self):
		pyVersion = eval(self.__dom.getAttribute("pyversion"))
		strVersion = str(pyVersion[0]) + "." + str(pyVersion[1]) + "."
		strVersion += str(pyVersion[2]) + " - " + str(pyVersion[3])

		return strVersion
	
	def getPythonAPIVersion(self):
		return self.__dom.getAttribute("pyapiversion")

	def getPyCrashVersion(self):
		return self.__dom.getAttribute("version")

	def getTimeAppCrashed(self):
		time = self.__dom.getAttribute("crashed") 
		return _strftime("%A %B %d %X - %Y", eval(time))
	
	def getTimeAppStarted(self):
		time = self.__dom.getAttribute("started") 
		return _strftime("%A %B %d %X - %Y", eval(time))

	def toHTML(self):
		osinfo = self.getOsInfo()
		html = "<div class=\"maininfo\">\n"
		html += "\t<table>\n\t<tr>\n"
		html += ("\t\t<td><b>Application Name</b>: <span class=\"data\">%s</span></td>\n" % self.getAppName())
		html += ("\t\t<td><b>Application Version</b>: <span class=\"data\">%s</span></td>\n" % self.getAppVersion())
		html += "\t</tr>\n\t<tr>\n"
		html += ("\t\t<td><b>Started on</b>: <span class=\"data\">%s</span></td>\n" % self.getTimeAppStarted())
		html += ("\t\t<td><b>Crashed on</b>: <span class=\"data\">%s</span></td>\n" % self.getTimeAppCrashed())
		
		html += "\t</tr>\n\t<tr>\n"
		html += ("\t\t<td><b>OS Type</b>: <span class=\"data\">%s</span></td>\n" % (osinfo[0] +" "+ osinfo[2] + " on " + osinfo[4]))
		html += ("\t\t<td><b>Host Name</b>: <span class=\"data\">%s</span></td>\n" % osinfo[1])
		
		html += "\t</tr>\n\t<tr>\n"
		html += ("\t\t<td><b>Python Version</b>: <span class=\"data\">%s</span></td>\n" % self.getPythonVersion())
		html += ("\t\t<td><b>Python Standard Lib Version</b>: <span class=\"data\">%s</span></td>\n" % self.getPythonAPIVersion())
		
		html += "\t</tr>\n\t<tr>\n"
		html += ("\t\t<td><b>PyCrash Version</b>: <span class=\"data\">%s</span></td>\n" % self.getPyCrashVersion())
		html += "\t\t<td></td>\n"
		html += "\t</tr>\n\t</table>\n\t<br />\n"

		cr = self.getCustomRecords()
		if len(cr) > 0:
			html += "\t<br />\n"		
			html += "\t<table>\n\t<tr>\n"
			html += "\t\t<td colspan=\"2\"><b>User defined Custom Records:</b></td>\n\t</tr>"
			
			i = 1
			for record in cr:
				html += ("\t<tr>\n\t\t<td><b>Custom Record %s:</b></td>\n" % i)
				html += ("\t\t<td>%s</td>\n\t</tr>\n" % record)
				i += 1
			
			html += "\t</table>\n\t<br />"

		html += "</div><!-- maininfo -->\n"
		for exc in self.__excTbList:
			html += exc.toHTML()
			html += "<br />"

		return html
		
	

class DumpParser:

	__initialized = 0
	
	def __init__(self):
		self.__dom = None
		self.__appData = None
		self.__initialized = 1

	def getAppData(self):
		return self.__appData

	def parseFile(self, filename):
		assert self.__initialized, "Document.__init__() not called"
		
		try:
			dom = _parse(filename)
		except IOError:
			raise
		except ExpatError: #this is not a well formed XML file
			raise Exception("The file \"" + filename + "\" is not a valid PyCrash crash dump file")
		else:
			self.__dom = dom
			self.__appData = AppData(self.__dom.getElementsByTagName("PyCrash")[0])

	def parseString(self, dump):
		try:
			dom = _parseString(dump)
		except ExpatError: #this is not a well formed XML string 
			raise Exception("This is not a valid PyCrash crash dump")
		else:
			self.__dom = dom
			self.__appData = AppData(self.__dom.getElementsByTagName("PyCrash")[0])
		

class HTMLPyCrash(pycrash.PyCrash):
	"""
		This class allows users to generate crash dump in HTML format.
	"""

	__initialized = 0
	DEFAULT_CSS = "http://pycrash.sf.net/htmldump/htmlpycrash.css"

	def __init__(self, strings):
		pycrash.PyCrash.__init__(self, strings)

		self.__appData = None
		self.__cssReference = self.DEFAULT_CSS
		self.__hideImg = 0

		self.__initialized = 1


	def __getHeaderHTML(self):
		header = """<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=ISO-8859-1" />
<style type="text/css" media="screen">
<!--
"""
	 	css = "@import url(\"%s\");" % self.__cssReference
		header += css
		if self.__hideImg:
			header += "\nimg { display: none }"
		header += """
-->
</style>"""
		
		title = "<title>PyCrash HTML dump of the application %s, version %s</title>" % (self.__appData.getAppName(), self.__appData.getAppVersion())
		header += title
		header += """
</head>
<body>
<p>%s</p>
<div id="bodyContent">\n"""
		return (header % self.getInfoText())

	def __getFooterHTML(self):
		footer = """
</div> <!-- bodyConent-->
<div id="footer">
	<p>&copy;Copyright Carmine I.D. Noviello 2004<br />
	<a href="http://validator.w3.org/check/referer">Valid XHTML 1.0</a>, <a href="http://jigsaw.w3.org/css-validator/validator?uri=http://www.pyj.it/pyj.css">Valid CSS</a>
 	</p>
</div><!-- footer --> 
</body>
</html>"""
		return footer

	def convertFileDump(self, filename):
		dumper = DumpParser();
		dumper.parseFile(filename);
		self.__appData = dumper.getAppData()

		htmlDump = self.__getHeaderHTML() 
		htmlDump += self.__appData.toHTML()
		htmlDump += self.__getFooterHTML()
		
		return htmlDump

	def convertStringDump(self, dumpString):
		dumper = DumpParser();
		dumper.parseString(dumpString)
		self.__appData = dumper.getAppData()

		htmlDump = self.__getHeaderHTML() 
		htmlDump += self.__appData.toHTML()
		htmlDump += self.__getFooterHTML()
		
		return htmlDump
		
	def getCrashDump(self):
		return self.convertStringDump( super(HTMLPyCrash, self).getCrashDump() )

	def getCSS(self):
		""" 
			Returns the reference to the main CSS 
		"""
		return self.__cssReference

	def hideImages(self, hide):
		assert type(hide) == type(0), "hide parameter must be an integer"
		"""
			This method can be used to hide/show images in the HTML dump
		"""
		self.__hideImg = hide

	def setCSS(self, css):
		""" 
			Set the reference to the main CSS 
		"""
		self.__cssReference = css

