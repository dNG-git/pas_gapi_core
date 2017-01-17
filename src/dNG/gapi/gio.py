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

# pylint: disable=import-error,no-name-in-module

from os import environ as os_env

class Gio(object):
    """
This class provides access to GIO related features.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.gapi
:subpackage: core
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;gpl
             GNU General Public License 2
    """

    @staticmethod
    def set_memory_settings_backend():
        """
Sets the "memory" backend to be used as the default one.

:since: v0.2.00
        """

        # pylint: disable=no-member

        os_env['GSETTINGS_BACKEND'] = "memory"
    #

    @staticmethod
    def set_memory_settings_backend_if_not_defined():
        """
Sets the "memory" backend to be used as the default one if no other one has
been defined.

:since: v0.2.00
        """

        # pylint: disable=no-member

        if (not "GSETTINGS_BACKEND" in os_env): Gio.set_memory_settings_backend()
    #
#
