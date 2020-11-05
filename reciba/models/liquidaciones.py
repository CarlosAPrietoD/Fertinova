# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'    
    
    deudor_titular_id = fields.Many2one('res.partner', string='Deudor Titular') 

class RecibaLiquidaciones(models.Model):
    _name = 'reciba.liquidaciones'
    _description = 'Liquidaciones de Reciba'

    @api.model_cr
    def init(self):
        #DELETE all content in model 'Reciba.Liquidaciones':
        self._cr.execute("""DELETE FROM reciba_liquidaciones""")
        
        conjunto = set()
        
        #Get invoices (only of client & provider type):
        facturas = self.env['account.invoice'].search([('state', '=', 'open'),
                                                        '|', ('type','=','out_invoice'),
                                                             ('type','=','in_invoice')])
        _logger.info('\n\n\n facturas ids: \n%s', facturas)
        #Invoices & bills Recorsets:
        facturas_recordsets = self.env['account.invoice'].browse(facturas.ids)
        #Put values into set in order to avoid repetitions:
        for factura in facturas_recordsets:
            conjunto.add(factura.partner_id.id)
        _logger.info('\n\n\n conjunto: \n%s', conjunto)

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #  Get debtors & creditors:

        #\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
        # Debtors Process:
        '''
        self._cr.execute("""SELECT ap.x_studio_contacto_deudor_acreedor_1 AS deudor, 
                                   ap.journal_id, aj.name, SUM(ap.amount)
                              FROM account_payment AS ap
                              JOIN account_journal AS aj ON ap.journal_id = aj.id
                             WHERE aj.name LIKE '%Deudor%' OR 
                                   aj.name LIKE '%BBVA%'
                             GROUP BY deudor, ap.journal_id, aj.name;""")
        '''
                          
        #Creation of records for model Reciba Liquidaciones from values in set:
        for item in conjunto:
            liquidaciones_pendientes = {
                'contacto_id': item,
            }
            self.env['reciba.liquidaciones'].create(liquidaciones_pendientes)                   
          

    contacto_id              = fields.Many2one('res.partner', string='Contacto')
    facturas_clientes_ids    = fields.One2many('account.invoice', 'id', string='Facturas de Cliente', compute='_set_facturas_clientes')
    deudores_ids             = fields.One2many('account.payment', 'id', string='Deudores', compute='_set_deudores')
    facturas_proveedores_ids = fields.One2many('account.invoice', 'id', string='Facturas de Proveedores', compute='_set_facturas_proveedores')
    acreedores_ids           = fields.One2many('account.payment', 'id', string='Acreedores', compute='_set_acreedores')
    saldo                    = fields.Float(string='Saldo', digits=(12,2), compute='_set_saldo')    


    @api.multi
    @api.depends('contacto_id')
    def _set_facturas_clientes(self):
        for rec in self:
            rec.facturas_clientes_ids = self.env['account.invoice'].search([('state', '=', 'open'),
                                                                            ('type','=','out_invoice'),
                                                                            ('partner_id','=', rec.contacto_id.id)])

    def _set_deudores(self):
        pass

    
    @api.multi
    @api.depends('contacto_id')
    def _set_facturas_proveedores(self):
        for rec in self:
            rec.facturas_proveedores_ids = self.env['account.invoice'].search([('state', '=', 'open'),
                                                                               ('type','=','in_invoice'),
                                                                               ('partner_id','=', rec.contacto_id.id)])
    
    def _set_acreedores(self):
        pass  

    @api.one
    @api.depends('contacto_id')
    def _set_saldo(self):
        total = 0.0
        
        total += sum(line.amount_total for line in self.facturas_clientes_ids)
        total += sum(line.amount for line in self.deudores_ids)
        #These ones must be negative:
        total += sum(line.amount_total for line in self.facturas_proveedores_ids)
        total += sum(line.amount for line in self.acreedores_ids)
        print(total)                       

        self.saldo = total                           
