# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;gapi;core

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
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;gpl
----------------------------------------------------------------------------
#echo(pasGapiCoreVersion)#
#echo(__FILEPATH__)#
"""

# pylint: disable=import-error,invalid-name,no-name-in-module

from weakref import ref

from dNG.data.logging.log_line import LogLine
from dNG.gapi.gio import Gio
from dNG.module.named_loader import NamedLoader
from dNG.plugins.hook import Hook
from dNG.runtime.exception_log_trap import ExceptionLogTrap
from dNG.runtime.instance_lock import InstanceLock
from dNG.runtime.thread import Thread
from dNG.runtime.value_exception import ValueException

from gi.repository import GLib

class GlibThread(Thread):
    """
This class implements a GLib main loop based singleton.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    # pylint: disable=arguments-differ,unused-argument

    _lock = InstanceLock()
    """
Thread safety lock
    """
    _weakref_instance = None
    """
GlibThread weakref instance
    """

    def __init__(self):
        """
Constructor __init__(GlibThread)

:since: v0.2.00
        """

        Thread.__init__(self)

        self.log_handler = NamedLoader.get_singleton("dNG.data.logging.LogHandler", False)
        """
The LogHandler is called whenever debug messages should be logged or errors
happened.
        """
        self.mainloop = None
        """
Active mainloop instance
        """

        Hook.register_weakref("dNG.pas.Status.onShutdown", self.stop)
    #

    def __del__(self):
        """
Destructor __del__(GlibThread)

:since: v0.2.00
        """

        if (self.mainloop is not None):
            self.stop()
        #
    #

    def run(self):
        """
Worker loop

:since: v0.2.00
        """

        # pylint: disable=broad-except

        mainloop = None

        with GlibThread._lock:
            if (self.mainloop is None):
                mainloop = GLib.MainLoop()
                self.mainloop = mainloop
            #
        #

        if (mainloop is not None):
            if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.run()- (#echo(__LINE__)#)", self, context = "pas_gapi_core")

            try: mainloop.run()
            except Exception as handled_exception: LogLine.error(handled_exception, context = "pas_gapi_core")
            except KeyboardInterrupt: Hook.call("dNG.pas.Status.stop")
            finally: self.stop()
        #
    #

    def start(self, params = None, last_return = None):
        """
Start the GLib based main loop in a separate thread.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.2.00
        """

        if (self.mainloop is None): Thread.start(self)
        return last_return
    #

    def stop(self, params = None, last_return = None):
        """
Stop the running GLib based main loop.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:since: v0.2.00
        """

        if (self.mainloop is not None):
            # Thread safety
            with GlibThread._lock:
                if (self.mainloop is not None):
                    if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.stop()- (#echo(__LINE__)#)", self, context = "pas_gapi_core")

                    if (self.mainloop.is_running()):
                        with ExceptionLogTrap("pas_gapi_core"): self.mainloop.quit()
                    #

                    self.mainloop = None

                    Hook.unregister("dNG.pas.Status.onShutdown", self.stop)
                #
            #
        #

        return last_return
    #

    @staticmethod
    def get_instance():
        """
Get the GLib based main loop singleton.

:return: (GlibThread) Object on success
:since:  v0.2.00
        """

        _return = (None
                   if (GlibThread._weakref_instance is None) else
                   GlibThread._weakref_instance()
                  )

        if (_return is None):
            with GlibThread._lock:
                # Thread safety

                if (GlibThread._weakref_instance is None): Gio.set_memory_settings_backend_if_not_defined()
                else: _return = GlibThread._weakref_instance()

                if (_return is None):
                    _return = GlibThread()
                    _return.start()

                    GlibThread._weakref_instance = ref(_return)
                #
            #
        #

        return _return
    #

    @staticmethod
    def mainloop_call(method, *args, **kwargs):
        """
The given method will be executed in the GLib main loop thread. Please
note that multiple keyword arguments are not supported.

:param method: Python callable

:since: v0.2.00
    """

        if (len(kwargs) > 1): raise ValueException("Multiple keyword arguments are not supported in the method iterator.")

        for key in kwargs: args += ( kwargs[key], )
        GLib.idle_add(method, *args)
    #
#

def glib_thread_mainloop_call(callback):
    """
This decorator is used to run the given callback in the GLib main loop
thread. Please note that multiple keyword arguments are not supported.

:param callback: Decoratable callback

:since: v0.2.00
    """

    def decorator(*args, **kwargs): GlibThread.mainloop_call(callback, *args, **kwargs)
    return decorator
#
