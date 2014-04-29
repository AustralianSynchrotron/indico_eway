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

from MaKaC.epayment import BaseEPayMod, BaseTransaction
import MaKaC.webinterface.urlHandlers as urlHandlers
from MaKaC.webinterface.common.tools import strip_ml_tags
from MaKaC.plugins import PluginsHolder, Plugin

from MaKaC.plugins.EPayment.eWay.webinterface import urlHandlers as localUrlHandlers
from MaKaC.plugins.EPayment.eWay import MODULE_ID

import requests
import xml.etree.ElementTree as ET
import json

class EWayMod(BaseEPayMod):

    def __init__(self, data=None):
        BaseEPayMod.__init__(self)
        self._title = "eWay"

        if data is not None:
            setValue(data)

    def getId(self):
        return MODULE_ID

    def clone(self, newSessions):
        sesf = EWayMod()
        sesf.setTitle(self.getTitle())
        sesf.setEnabled(self.isEnabled())
        return sesf

    def setValues(self, data):
        self.setTitle(data.get("title", "epayment"))

    def getUrl(self):
        ph = PluginsHolder()
        return ph.getPluginType("EPayment").getPlugin("eWay").getOption("url").getValue()

    def getCustomerID(self):
        ph = PluginsHolder()
        return ph.getPluginType("EPayment").getPlugin("eWay").getOption("customer_id").getValue()

    def getCustomerUsername(self):
        ph = PluginsHolder()
        return ph.getPluginType("EPayment").getPlugin("eWay").getOption("customer_username").getValue()

    def getFormHTML(self, prix, currency, conf, registrant, lang = "en_GB", secure=False):
        conference = registrant.getConference()
        eway_data = {
            'CustomerID': self.getCustomerID(),
            'UserName':   self.getCustomerUsername(),
            'Amount':     "%.2f"%prix,
            'Currency':   currency,
            'MerchantReference': "indico_%s_%s" % (conference.getId(), registrant.getId()),
            'MerchantInvoice':  "indico_%s_%s" % (conference.getId(), registrant.getId()),
            'InvoiceDescription': "Invoice for: %s - %s" % (conference.getTitle(), conference.getDescription()),
            'ReturnURL':  "%s"%localUrlHandlers.UHPayConfirmEWay.getURL(registrant),
            'CancelURL':  "%s"%localUrlHandlers.UHPayCancelEWay.getURL(registrant)
        }

        r = requests.get(self.getUrl(), params=eway_data)
        transaction_url = ET.fromstring(r.text).find('URI')
        if transaction_url == None:
            raise Exception(r.text)

        return '<form action="%s" method="POST" id="%s"></form>'%(transaction_url.text, self.getId())


    def getConfModifEPaymentURL(self, conf):
        return localUrlHandlers.UHConfModifEPaymentEWay.getURL(conf)



class TransactionEWay(BaseTransaction):

    def __init__(self,parms):
        BaseTransaction.__init__(self)
        self._Data = parms

    def getId(self):
        try:
            if self._id:
                pass
        except AttributeError, e:
            self._id="eWay"
        return self._id

    def getId(self):
        return self._id

    def getTransactionHTML(self):
        #return"""<table>
        #                  <tr>
        #                    <td align="right"><b>Payment with:</b></td>
        #                    <td align="left">PayPal</td>
        #                  </tr>
        #                  <tr>
        #                    <td align="right"><b>Payment Date:</b></td>
        #                    <td align="left">%s</td>
        #                  </tr>
        #                  <tr>
        #                    <td align="right"><b>Payment ID:</b></td>
        #                    <td align="left">%s</td>
        #                  </tr>
        #                  <tr>
        #                    <td align="right"><b>Order Total:</b></td>
        #                    <td align="left">%s %s</td>
        #                  </tr>
        #                  <tr>
        #                    <td align="right"><b>verify sign:</b></td>
        #                    <td align="left">%s</td>
        #                  </tr>
        #                </table>"""%(self._Data["payment_date"],self._Data["payer_id"], self._Data["mc_gross"], \
        #                     self._Data["mc_currency"], self._Data["verify_sign"])
        return json.dumps(self._Data)

    def getTransactionTxt(self):
        return json.dumps(self._Data)
#        return"""
#\tPayment with:PayPal\n
#\tPayment Date:%s\n
#\tPayment ID:%s\n
#\tOrder Total:%s %s\n
#\tverify sign:%s
#"""%(self._Data["payment_date"],self._Data["payer_id"], self._Data["mc_gross"], \
#                             self._Data["mc_currency"], self._Data["verify_sign"])



def getPayMod():
    return EWayMod()

def getPayModClass():
    return EWayMod
