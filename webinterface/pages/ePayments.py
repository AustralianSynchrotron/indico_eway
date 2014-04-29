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

import MaKaC.webinterface.pages.conferences as conferences
import MaKaC.webinterface.pages.registrationForm as registrationForm
from MaKaC.webinterface import wcomponents
from xml.sax.saxutils import quoteattr
from MaKaC.common import Configuration
from MaKaC.webinterface import urlHandlers
import MaKaC
from MaKaC.i18n import _


from MaKaC.plugins.EPayment.eWay import MODULE_ID
from MaKaC.plugins.EPayment.eWay.webinterface.wcomponents import WTemplated
from MaKaC.plugins.EPayment.eWay.webinterface import urlHandlers as localUrlHandlers



class WPConfModifEPaymentEWayBase(registrationForm.WPConfModifRegFormBase):

    def _createTabCtrl( self ):
        self._tabCtrl = wcomponents.TabControl()
        self._tabMain = self._tabCtrl.newTab( "main", _("Main"), \
                localUrlHandlers.UHConfModifEPaymentEWay.getURL( self._conf ) )
        wf = self._rh.getWebFactory()
        if wf:
            wf.customiseTabCtrl( self._tabCtrl )
        self._setActiveTab()

    def _setActiveTab( self ):
        pass

    def _setActiveSideMenuItem(self):
        self._regFormMenuItem.setActive(True)

    def _getPageContent( self, params ):
        self._createTabCtrl()
        banner = wcomponents.WEpaymentBannerModif(self._conf.getModPay().getPayModByTag(MODULE_ID), self._conf).getHTML()
        html = wcomponents.WTabControl( self._tabCtrl, self._getAW() ).getHTML( self._getTabContent( params ) )
        return banner+html

    def _getTabContent( self, params ):
        return "nothing"

class WPConfModifEPaymentEWay( WPConfModifEPaymentEWayBase ):
    
    def _getTabContent( self, params ):
        wc = WConfModifEPaymentEWay(self._conf)
        p = {
             'dataModificationURL': quoteattr(str(localUrlHandlers.UHConfModifEPaymentEWayDataModif.getURL( self._conf )))
            }
        return wc.getHTML(p)

class WConfModifEPaymentEWay( WTemplated ):
    
    def __init__( self, conference ):
        self._conf = conference

    def getVars( self ):
        vars = WTemplated.getVars(self)
        modEWay = self._conf.getModPay().getPayModByTag(MODULE_ID)
        vars["title"] = modEWay.getTitle()
        vars["url"] = modEWay.getUrl()
        vars["customer_id"] = modEWay.getCustomerID()
        vars["customer_username"] = modEWay.getCustomerUsername()
        return vars

class WPConfModifEPaymentEWayDataModif( WPConfModifEPaymentEWayBase ):
    
    def _getTabContent( self, params ):
        wc = WConfModifEPaymentEWayDataModif(self._conf)
        p = {'postURL': quoteattr(str(localUrlHandlers.UHConfModifEPaymentEWayPerformDataModif.getURL( self._conf )))
            }
        return wc.getHTML(p)

class WConfModifEPaymentEWayDataModif( WTemplated ):
    
    def __init__( self, conference ):
        self._conf = conference

    def getVars( self ):
        vars = WTemplated.getVars(self)
        modEWay = self._conf.getModPay().getPayModByTag(MODULE_ID)
        vars["title"] = modEWay.getTitle()
        vars["url"] = modEWay.getUrl()
        vars["customer_id"] = modEWay.getCustomerID()
        vars["customer_username"] = modEWay.getCustomerUsername()
        return vars

class WPconfirmEPaymentEWay( conferences.WPConferenceDefaultDisplayBase ):
    #navigationEntry = navigation.NERegistrationFormDisplay

    def __init__(self, rh, conf, reg):
        conferences.WPConferenceDefaultDisplayBase.__init__(self, rh, conf)
        self._registrant=reg
        
        
    def _getBody( self, params ):
        wc = WconfirmEPaymentEWay(self._conf, self._registrant)
        return wc.getHTML()

    def _defineSectionMenu( self ): 
        conferences.WPConferenceDefaultDisplayBase._defineSectionMenu(self)
        self._sectionMenu.setCurrentItem(self._regFormOpt)
        
        
class WconfirmEPaymentEWay( WTemplated ):
    def __init__( self,configuration, registrant):
        self._registrant = registrant
        self._conf = configuration
        
    def getVars( self ):
        vars = WTemplated.getVars(self)
        vars["message"] = "Thank you for the payment!<br/> You have used EWay"
        vars["trinfo"]="%s:%s"%(self._registrant.getFirstName(),self._registrant.getSurName())
        return vars
 
class WPCancelEPaymentEWay( conferences.WPConferenceDefaultDisplayBase ):
    #navigationEntry = navigation.NERegistrationFormDisplay

    def __init__(self, rh, conf, reg):
        conferences.WPConferenceDefaultDisplayBase.__init__(self, rh, conf)
        self._registrant=reg
        
    def _getBody( self, params ):
        wc = WCancelEPaymentEWay( self._conf,self._registrant )
        return wc.getHTML()

    def _defineSectionMenu( self ): 
        conferences.WPConferenceDefaultDisplayBase._defineSectionMenu(self)
        self._sectionMenu.setCurrentItem(self._regFormOpt)    
        
class WCancelEPaymentEWay( WTemplated ):
    def __init__( self, conference,reg ):
        self._conf = conference
        self._registrant=reg

    def getVars( self ):
        vars = WTemplated.getVars(self)
        vars["message"] = "You have cancelled your transaction.\nPlease check your email in order to complete your eWay transaction."
        vars["messagedetailPayment"]="%s:%s"%(self._registrant.getFirstName(),self._registrant.getSurName())
        return vars 
