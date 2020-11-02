# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class RecibaLiquidaciones(models.Model):
    _name = 'reciba.liquidaciones'
    _description = 'Liquidaciones de Reciba'

    @api.model_cr
    def init(self):
        #DELETE all content in model 'Reciba.Liquidaciones':
        self._cr.execute("""DELETE FROM reciba_liquidaciones""")

        #Get invoices and loans:
        facturas = self.env['account.invoice'].search([('state', '=', 'open'),
                                                        '|', ('type','=','out_invoice'),
                                                             ('type','=','in_invoice')])
        print('\n\n\n facturas ids: ', facturas)
        _logger.info('\n\n\n facturas ids: \n%s', facturas)

        prestamos = self.env['reciba.prestamos'].search([('state', '=', 'open')])
        print('\n\n\n prestamos ids: ', prestamos)
        _logger.info('\n\n\n prestamos ids: \n%s', prestamos)
        _logger.info('\n\n\n prestamos ids con .ids: \n%s', prestamos.ids)

        #Obtain and Iterate recordsets from Invoices and Loans in order to fill model of Liquidaciones:
        facturas_recordsets = self.env['account.invoice'].browse(facturas.ids)
        for factura in facturas_recordsets:
            if factura.type == 'out_invoice':
                tipo = 'Factura Cliente'
            elif factura.type == 'in_invoice':
                tipo = 'Factura Proveedor'
                factura.amount_total = factura.amount_total * -1

            #Retrieve deudor_titular from partner_id:
            contacto_titular = self.env['res.partner'].search([('id','=',factura.partner_id.id)]).deudor_titular_id.id                 
            _logger.info('\n\n\n contacto_titular: \n%s', contacto_titular)

            liquidaciones_pendientes = {
                'tipo_operacion': tipo,
                'referencia': factura.number,
                'contacto_id': contacto_titular,
                'cantidad': factura.amount_total,
                'fecha': factura.date_invoice,
                'estado': 'Abierto'
            }
            self.env['reciba.liquidaciones'].create(liquidaciones_pendientes)

        prestamos_recordsets = self.env['reciba.prestamos'].browse(prestamos.ids)
        for prestamo in prestamos_recordsets:
            #Retrieve deudor_titular from contacto_id:
            contacto_titular = self.env['res.partner'].search([('id', '=', prestamo.contacto_id.id)]).deudor_titular_id.id             
            
            liquidaciones_pendientes = {
                'tipo_operacion': 'Préstamo',
                'referencia': prestamo.name,
                'contacto_id': contacto_titular,
                'cantidad': prestamo.cantidad,
                'fecha': prestamo.fecha_prestamo,
                'estado': 'Abierto'
            }
            self.env['reciba.liquidaciones'].create(liquidaciones_pendientes)        


    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #      FIELDS
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::    
    tipo_operacion = fields.Char(string='Tipo de Operación')
    referencia     = fields.Char(string='Referencia')
    contacto_id    = fields.Many2one('res.partner', string='Contacto')
    cantidad       = fields.Float(string='Cantidad', digits=dp.get_precision('Product Unit of Measure'))   
    fecha          = fields.Date(string='Fecha')
    estado         = fields.Char(string='Estado')
