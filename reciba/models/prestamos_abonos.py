# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'      

    def _set_abonos(self):
        pass     
    
    rec_abono_prestamo   = fields.Char(string='Concepto')
    tipo_movimiento      = fields.Selection([
                                             ('prestamo_deudor', 'Préstamo a Deudores Diversos'),
                                             ('abono_deudor', 'Abono a Deudores Diversos'),
                                             ('prestamo_acreedor', 'Préstamo a Acreedores Diversos'),
                                             ('abono_acreedor', 'Abono a Acreedores Diversos')
                                            ], string='Tipo de Préstamo/Abono', compute='_set_tipo')
    abonos_relacionados  = fields.One2many('account.payment', 'id', string='Abonos relacionados', default=_set_abonos)
    prestamo_relacionado = fields.Many2one('account.payment', string='')
    dias_transcurridos   = fields.Integer(string='', compute='_set_dias')
    interes_generado     = fields.Float(string='Interés', digits=(15,2), compute='_set_interes')    
    saldo_computado      = fields.Float(string='Saldo Computado', digits=(15,2), compute='_set_saldo_computado') 

    @api.one
    @api.depends('journal_id')
    def _set_tipo(self):
        pass
        """
        #Get IDs for BBVA Bank & Deudores Diversos (MXN):
        journal_id_deudores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_deudores %s\n\n', journal_id_deudores)

        journal_id_acreedores = self.env['account.journal'].search([('name', 'ilike', 'Acreedores diversos')])
        _logger.info('\n journal_id_acreedores %s\n\n', journal_id_acreedores)      

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'Bank')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco) 

        if self.journal_id.id in journal_id_banco.ids and self.destination_journal_id.id in journal_id_deudores.ids:
            self.tipo_movimiento = 'prestamo_deudor'

        elif self.destination_journal_id.id in journal_id_deudores.ids and self.journal_id.id in journal_id_banco.ids:                     
            self.tipo_movimiento = 'abono_deudor'

        elif self.journal_id.id in journal_id_banco.ids and self.destination_journal_id.id in journal_id_acreedores.ids:
            self.tipo_movimiento = 'abono_acreedor'

        elif self.destination_journal_id.id in journal_id_acreedores.ids and self.journal_id.id in journal_id_banco.ids:                     
            self.tipo_movimiento = 'prestamo_acreedor'   
        """             
    
    
    @api.one
    def _set_dias(self):
        pass


    @api.one
    def _set_interes(self):
        pass


    @api.one
    def _set_saldo_computado(self):
        pass