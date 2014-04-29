# -*- coding: utf-8 -*-
##
##
## This file is part of Indico.
## Copyright (C) 2002 - 2013 European Organization for Nuclear Research (CERN).
##
## Indico is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 3 of the
## License, or (at your option) any later version.
##
## Indico is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Indico;if not, see <http://www.gnu.org/licenses/>.
from MaKaC.i18n import _

#eWay payment plugin options
globalOptions = [
    ("url", {"description" : _("Request URL for eWay"),
             "type": str,
             "defaultValue": "https://au.ewaygateway.com/Request",
             "editable": True,
             "visible": True,
             "mustReload": False}
    ),
    ("customer_id", {"description" : _("Customer ID"),
                     "type": str,
                     "defaultValue": "87654321",
                     "editable": True,
                     "visible": True,
                     "mustReload": False}
    ),
    ("customer_username", {"description" : _("Customer Username"),
                           "type": str,
                           "defaultValue": "TestAccount",
                           "editable": True,
                           "visible": True,
                           "mustReload": False}
    )
]
