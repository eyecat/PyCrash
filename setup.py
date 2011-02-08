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

#!/usr/bin/env python

from distutils.core import setup

setup(  name="PyCrash",
      	version="0.4-pre3",
		description="PyCrash: a Run-Time Exception Dumper for Python programs",
		author="Carmine I.D. Noviello",
		author_email="cnoviello@pycrash.org",
		url="http://www.pycrash.org",
		packages=['pycrash', 'pycrash.utils'],
		scripts = ['utils/keygen.py', 'utils/decrypt.py', 'utils/pycrash2html.py']
)
