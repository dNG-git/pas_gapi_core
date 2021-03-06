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

from dNG.runtime.result_event import ResultEvent

class CallbackContextMixin(object):
    """
"CallbackContextMixin" provides a context manager for handling gapi mainloop
callbacks and signal based thread synchronization.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    def __init__(self):
        """
Constructor __init__(CallbackContextMixin)

:since: v0.2.00
        """

        self._callback_result_event = None
        """
Callback result delivering event
        """
    #

    def __enter__(self):
        """
python.org: Enter the runtime context related to this object.

:since: v0.2.00
        """

        self._callback_result_event = ResultEvent()
        return self
    #

    def __exit__(self, exc_type, exc_value, traceback):
        """
python.org: Exit the runtime context related to this object.

:return: (bool) True to suppress exceptions
:since:  v0.2.00
        """

        if (self._callback_result_event is not None): self._callback_result_event.set()
        return False
    #
#
