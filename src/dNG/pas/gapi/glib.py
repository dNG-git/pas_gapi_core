# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.gapi.Glib
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;gapi;core

The following license agreement remains valid unless any additions or
changes are being made by direct Netware Group in a written form.

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;gpl
----------------------------------------------------------------------------
#echo(pasGapiCoreVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

# pylint: disable=import-error,no-name-in-module

from gi.repository import GLib as GiGLib

class Glib(object):
#
	"""
This class has been designed to provide static methods for introspected GLib
data.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	@staticmethod
	def get_gquark_string(_id):
	#
		"""
Returns the string associated with the given GQuark ID.

:param _id: GQuark ID

:return: (str) Associated string
:since:  v0.1.00
		"""

		# pylint: disable=no-member

		return GiGLib.quark_to_string(_id)
	#

	@staticmethod
	def parse_glist(glist):
	#
		"""
Parses and returns a list.

:param glist: GLib GList data, Python list or convertable data.

:return: (list) Python list
:since:  v0.1.00
		"""

		_type = type(glist)

		if (_type == GiGLib.List):
		#
			_return = [ ]
			for i in range(0, glist.length()): _return.append(glist.nth(i))
		#
		elif (_type == list): _return = glist
		else: _return = list(glist)

		return _return
	#
#

##j## EOF