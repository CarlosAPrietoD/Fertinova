# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _  

import logging
_logger = logging.getLogger(__name__)

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class report_account_aged_receivable(models.AbstractModel):
    _inherit = "account.aged.receivable"

    def _get_columns_name(self, options):    
        columns = super()_get_columns_name(options)
        columns.insert(4, {'name': _('Invoice Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'})
        return columns
    
    def _get_lines(self, options, line_id=None):  
        pass      
        
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  