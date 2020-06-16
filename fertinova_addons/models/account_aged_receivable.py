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
        """This method intends add a new column of Invoice Date into Account Aged Receivable Report"""
        columns = super()._get_columns_name(options)
        columns.insert(4, {'name': _('Invoice Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'})
        return columns
    
    @api.model
    def _get_lines(self, options, line_id=None):
        lines = super()._get_lines(options, line_id)

     
        
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  
lines: [ 
         {
          'id': 'partner_3918', 
          'name': 'AGROFOS S DE RL DE CV', 
          'level': 2, 
          'columns': [
                      {'name': ''}, 
                      {'name': ''}, 
                      {'name': ''}, 
                      {'name': '$ 73,905.34'}, 
                      {'name': '$ 0.00'}, 
                      {'name': '$ 0.00'}, 
                      {'name': '$ 0.00'}, 
                      {'name': '$ 0.00'}, 
                      {'name': '$ 0.00'}, 
                      {'name': '$ 73,905.34'}
                     ], 
          'trust': 'normal', 
          'unfoldable': True, 
          'unfolded': True
          }, 
          {
           'id': 154380, 
           'name': '27/06/2020', 
           'class': 'date', 
           'caret_options': 
           'account.invoice.out', 
           'level': 4, 
           'parent_id': 'partner_3918', 
           'columns': [
                       {'name': 'FC'}, 
                       {'name': '105.01.001'}, 
                       {'name': 'FC3684-FC3684/95'}, 
                       {'name': '$ 36,620.42'}, 
                       {'name': ''}, 
                       {'name': ''}, 
                       {'name': ''}, 
                       {'name': ''}, 
                       {'name': ''}, 
                       {'name': ''}
                      ], 
           'action_context': {
                              'default_type': 'out_invoice', 
                              'default_journal_id': 41
                              }
           }, 
           {
            'id': 155735, 
            'name': '30/06/2020', 
            'class': 'date', 
            'caret_options': 'account.invoice.out', 
            'level': 4, 
            'parent_id': 'partner_3918', 
            'columns': [
                        {'name': 'FC'}, 
                        {'name': '105.01.001'}, 
                        {'name': 'FC3688-FC3688/02'}, 
                        {'name': '$ 37,284.92'}, 
                        {'name': ''}, 
                        {'name': ''}, 
                        {'name': ''}, 
                        {'name': ''}, 
                        {'name': ''}, 
                        {'name': ''}
                       ], 
            'action_context': {
                               'default_type': 'out_invoice', 
                               'default_journal_id': 41
                               }
            } 
           ]