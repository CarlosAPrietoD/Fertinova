# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = 'account.payment'    
    
    rec_abono_prestamo   = fields.Char(string='Concepto')
    tipo_movimiento      = fields.Selection([
                                             ('prestamo_deudor', 'Deudores Diversos Préstamo'),
                                             ('abono_deudor', 'Deudores Diversos Abono'),
                                             ('prestamo_acreedor', 'Acreedores Diversos Préstamo'),
                                             ('abono_acreedor', 'Acreedores Diversos Abono')
                                            ], string='Tipo de Préstamo/Abono')
    abonos_relacionados  = fields.One2many('account.payment', 'id', string='Abonos relacionados')
    prestamo_relacionado = fields.Many2one('account.payment', string='')
    dias_transcurridos   = fields.Integer(string='')
    interes_generado     = fields.Float(string='Interés', digits=(15,2))    
    saldo_computado      = fields.Float(string='Saldo Computado', digits=(15,2)) 
    
