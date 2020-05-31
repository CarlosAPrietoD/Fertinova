# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _  

import logging
_logger = logging.getLogger(__name__)

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountFollowupReport(models.AbstractModel):
    _inherit = 'account.followup.report'

    #########################################################
    # MODEL METHODS
    #########################################################
    def _get_columns_name(self, options):
        """This method intends to add a new column into Account Payable Report"""
        #Sample about what is inside in headers list:   
        #headers = [{},
        #           {'name': _('Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
        #           {'name': _('Due Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
        #           {'name': _('Source Document'), 'style': 'text-align:center; white-space:nowrap;'},
        #           {'name': _('Communication'), 'style': 'text-align:right; white-space:nowrap;'},
        #           {'name': _('Expected Date'), 'class': 'date', 'style': 'white-space:nowrap;'},
        #           {'name': _('Excluded'), 'class': 'date', 'style': 'white-space:nowrap;'},
        #           {'name': _('Total Due'), 'class': 'number o_price_total', 'style': 'text-align:right; white-space:nowrap;'}
        #          ]     
            
        #Retrieve original list:
        headers = super(AccountFollowupReport, self)._get_columns_name(options)
        #Add new column of Invoice Date:
        headers.insert(2, {'name': _('Invoice Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'})

        return headers
        
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  