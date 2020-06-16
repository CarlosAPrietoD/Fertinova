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
        columns = super()._get_columns_name(options)
        columns.insert(4, {'name': _('Invoice Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'})
        return columns
    
    def _get_lines(self, options, line_id=None):  
        #This button construct a dictionary which eventually inserted into a list
        vals: {'id': 142364, 
               'name': '25/05/2020', 
               'class': 'date', 
               'caret_options': 'account.invoice.out', 
               'level': 4, 
               'parent_id': 'partner_525', 
               'columns': [
                   {'name': 'FC'}, 
                   {'name': '105.01.001'}, 
                   {'name': 'FC9265-FC9265/50'}, 
                   {'name': ''}, 
                   {'name': '$ 208,498.40'}, 
                   {'name': ''}, {'name': ''}, 
                   {'name': ''}, {'name': ''}, 
                   {'name': ''}
                ], 
                'action_context': {'default_type': 'out_invoice', 'default_journal_id': 1}
              }

        lines: [
                {'id': 'partner_525', 
                'name': 'AGROPECUARIA EL GRAN CHAPARRAL SA DE CV', 
                'level': 2, 
                'columns': [
                            {'name': ''},         {'name': ''}, 
                            {'name': ''},         {'name': '$ 0.00'}, 
                            {'name': '$ 1,086,591.00'}, 
                            {'name': '$ 0.00'},   {'name': '$ 0.00'}, 
                            {'name': '$ 0.00'},   {'name': '$ 0.00'}, 
                            {'name': '$ 1,086,591.00'}
                           ], 
                           'trust': 'normal',     'unfoldable': True,       'unfolded': True
                }, 
                {'id': 142364, 'name': '25/05/2020', 
                'class': 'date', 
                'caret_options': 'account.invoice.out', 'level': 4, 
                'parent_id': 'partner_525', 
                'columns': [
                            {'name': 'FC'},       {'name': '105.01.001'}, 
                            {'name': 'FC9265-FC9265/50'}, 
                            {'name': ''},         {'name': '$ 208,498.40'}, 
                            {'name': ''},         {'name': ''}, 
                            {'name': ''},         {'name': ''}, 
                            {'name': ''}
                           ], 
                'action_context': {'default_type': 'out_invoice', 'default_journal_id': 1}
                }
              ]        

        pass      
        
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  