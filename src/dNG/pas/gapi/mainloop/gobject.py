# -*- coding: utf-8 -*-
##j## BOF

"""
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
"""

# pylint: disable=import-error,invalid-name,no-name-in-module

from gi.repository import GLib
from gi.repository import GObject as GiGObject
from weakref import ref

from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.exception_log_trap import ExceptionLogTrap
from dNG.pas.runtime.instance_lock import InstanceLock
from dNG.pas.runtime.thread import Thread
from dNG.pas.runtime.value_exception import ValueException

class Gobject(Thread):
#
	"""
This class implements a GObject mainloop singleton.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: core
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;gpl
             GNU General Public License 2
	"""

	# pylint: disable=arguments-differ,unused-argument

	_lock = InstanceLock()
	"""
Thread safety lock
	"""
	_weakref_instance = None
	"""
GObject weakref instance
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Gobject)

:since: v0.1.00
		"""

		Thread.__init__(self)

		self.mainloop = None
		"""
Active mainloop instance
		"""

		Hook.register("dNG.pas.Status.onShutdown", self.stop)
	#

	def __del__(self):
	#
		"""
Destructor __del__(Gobject)

:since: v0.1.00
		"""

		self.stop()
	#

	def run(self):
	#
		"""
Worker loop

:since: v0.1.00
		"""

		# pylint: disable=broad-except

		self.mainloop = GiGObject.MainLoop()

		try: self.mainloop.run()
		except Exception as handled_exception: LogLine.error(handled_exception, context = "pas_gapi_core")
		except KeyboardInterrupt: Hook.call("dNG.pas.Status.stop")
		finally: self.stop()
	#

	def start(self, params = None, last_return = None):
	#
		"""
Start the GObject mainloop in a separate thread.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		if (self.mainloop == None): Thread.start(self)
		return last_return
	#

	def stop(self, params = None, last_return = None):
	#
		"""
Stop the running GObject mainloop.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.1.00
		"""

		if (self.mainloop != None):
		# Thread safety
			with Gobject._lock:
			#
				if (self.mainloop != None):
				#
					if (self.mainloop.is_running()):
					#
						with ExceptionLogTrap("pas_gapi_core"): self.mainloop.quit()
					#

					Hook.unregister("dNG.pas.Status.onShutdown", self.stop)
				#
			#
		#

		return last_return
	#

	@staticmethod
	def get_instance():
	#
		"""
Get the GObject singleton.

:return: (Gobject) Object on success
:since:  v0.1.00
		"""

		_return = None

		with Gobject._lock:
		#
			if (Gobject._weakref_instance != None): _return = Gobject._weakref_instance()

			if (_return == None):
			#
				_return = Gobject()
				_return.start()

				Gobject._weakref_instance = ref(_return)
			#
		#

		return _return
	#
#

def Gobject_mainloop_callback(callback):
#
	"""
This decorator is used to run the given callback in the GObject mainloop
thread. Please note that multiple keyword arguments are not supported.

:param callback: Decoratable callback

:since: v0.1.00
	"""

	def decorator(*args, **kwargs):
	#
		if (len(kwargs) > 1): raise ValueException("Multiple keyword arguments are not supported in the callback iterator.")

		for key in kwargs: args += ( kwargs[key], )
		GLib.idle_add(callback, *args)
	#

	return decorator
#

##j## EOF