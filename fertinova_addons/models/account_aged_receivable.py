# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _  

_logger = logging.getLogger(__name__)

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class report_account_aged_receivable(models.AbstractModel):
    _inherit = "account.aged.receivable"

    def _get_columns_name(self, options):    
        """This method intends add a new column of Invoice Dates into Account Aged Receivable Report"""
        #Obtain columns of original header:
        columns = super()._get_columns_name(options)
        #Inserting new column of Invoice Date:
        columns.insert(4, {'name': _('Invoice Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'})
        return columns
    
    @api.model
    def _get_lines(self, options, line_id=None):
        """This method intends add a new values of Invoice Dates into Account Aged Receivable Report"""
        #Obtain original list of rows of the report:
        lines = super()._get_lines(options, line_id)
        for line in lines:
            #Only the rows with level 4 correspond to broken down concepts:
            if line['level'] == 2:
                line.get('columns').insert(3, {'name': ''}) 
            elif line['level'] == 4:     
                #Get 'Reference' value which is like INVOICE-INVOICE/REF:           
                factura_aux = line['columns'][2].get('name')
                #Obtain just the part before -(hyphen):
                factura, residuo = factura_aux.split('-')
                _logger.info('\n\n\n factura: %s \n\n', factura)
                #Retrieve the of invoice date from model 'account.invoice':
                invoice_date = self.env['account.invoice'].search(['number','ilike', factura]).date_invoice
                _logger.info('\n\n\n invoice_date: %s \n\n', invoice_date)
                #Insert the new value in corresponding with the position of new columm added too:
                line.get('columns').insert(3, {'name': str(invoice_date)}) 
        return lines

    #SAMPLE OF A SINGLE ROW RETURNED BY ORIGINAL LIST "LINES":
    """    
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
    """                                    
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 116    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  