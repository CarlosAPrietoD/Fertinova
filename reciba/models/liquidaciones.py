# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'    
    
    deudor_titular_id = fields.Many2one('res.partner', string='Deudor Titular') 



class AccountPayment(models.Model):
    _inherit = 'account.payment'    
    
    rec_abono_prestamo = fields.Char(string='Concepto de abono/préstamo para auxilio de Reciba')



class RecibaLiquidaciones(models.Model):
    _name = 'reciba.liquidaciones'
    _description = 'Liquidaciones de Reciba'


    # !-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!
    # THIS METHOD GETS BENEFIT FOR INITIALIZING THE MODEL
    # First delete all records and retrieve data for process of open invoices
    # of Clients & Providers as well Payments and Loans to Debtors or Creditors:
    @api.model_cr
    def init(self):
        #DELETE all content in model 'Reciba.Liquidaciones':
        self._cr.execute("""DELETE FROM reciba_liquidaciones""")
        
        #Set to store records in order to avoid repeted values:
        conjunto = set()
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #Get Open Invoices (only of client & provider type):
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

        #Get IDs for BBVA Bank & Deudores Diversos (MXN):
        journal_id_deudores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_deudores %s\n\n', journal_id_deudores)

        journal_id_acreedores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_acreedores %s\n\n', journal_id_deudores)        

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'Bank')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        # Retrieve amounts grouped by x_studio_contacto_deudor_acreedor_1 
        # BOTH FOR LOANS & PAYMENTS:        
        # !-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!-!
        
        if journal_id_deudores and journal_id_acreedores and journal_id_banco:
            # A PAYMENT IS WHEN JOURNAL_ID IS A DEBTOR BRINGING MONEY TO COMPANY
            #  DEBTOR ======={$ money}=======> > COMPANY'S BANK
            grupo_abono_prestamos = self.env['account.payment'].read_group(
                domain=[('payment_type', '=', 'transfer'),                
                         '|', ('journal_id', 'in', journal_id_deudores.ids),
                         '|', ('journal_id', 'in', journal_id_acreedores.ids),
                              ('journal_id', 'in', journal_id_banco.ids),                         
                         '|', ('destination_journal_id', 'in', journal_id_deudores.ids),
                         '|', ('destination_journal_id', 'in', journal_id_acreedores.ids),
                              ('destination_journal_id', 'in', journal_id_banco.ids)],
                fields=['payment_date', 'name', 'partner_id', 'journal_id', 'destination_journal_id', 'communication', 'amount:sum', 'state'], 
                groupby=['partner_id'])
            _logger.info('\n\n grupo_abono_prestamos \n\n%s\n\n', grupo_abono_prestamos)
            #RESULT LOG:
            #[{'partner_id_count': 3, 'amount': 150.0, 'partner_id': (14, <odoo.tools.func.lazy object at 0x7fb0d4e1cc18>), '__domain': ['&', ('partner_id', '=', 14), '|', ('journal_id', 'in', [9]), ('destination_journal_id', 'in', [7])]}]
            
            #Put values into set in order to avoid repetitions:
            for i in grupo_abono_prestamos:
                if isinstance(i.get('partner_id'), bool):
                    print("evitar error por conseguir FALSE")
                else:            
                    debtor_id = i.get('partner_id')[0]
                    conjunto.add(debtor_id) 
                    print(debtor_id)
            _logger.info('\n\n\n conjunto: \n%s', conjunto)        
                    

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!         
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Creation of records for model Reciba Liquidaciones from values in set:
        for item in conjunto:
            liquidaciones_pendientes = {
                'contacto_id': item,
            }
            self.env['reciba.liquidaciones'].create(liquidaciones_pendientes)                   
          


    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    #  MODEL  FIELDS
    # //////////////////////////////////////////////////////////////////////////
    contacto_id = fields.Many2one('res.partner', string='Contacto')
    compania_id = fields.Many2one('res.company', string='Compañía', compute='_set_compania')

    facturas_clientes_ids = fields.One2many('account.invoice', 'id', string='Facturas de Cliente', compute='_set_facturas_clientes')
    
    deudores_general         = fields.One2many('account.payment', 'id', string='Deudores (General)', compute='_set_deudores_general')    
    deudores_ids_abonos      = fields.One2many('account.payment', 'id', string='Deudores (Abonos)', compute='_set_deudores_abonos')
    saldo_deudores_abonos    = fields.Float(string='Saldo Deudores Abonos', digits=(15,2), compute='_set_saldo_deudores_abonos')    
    deudores_ids_prestamos   = fields.One2many('account.payment', 'id', string='Deudores (Préstamos)', compute='_set_deudores_prestamos')
    saldo_deudores_prestamos = fields.Float(string='Saldo Deudores Préstamos', digits=(15,2), compute='_set_saldo_deudores_prestamos')
    
    facturas_proveedores_ids   = fields.One2many('account.invoice', 'id', string='Facturas de Proveedores', compute='_set_facturas_proveedores')
    saldo_facturas_proveedores = fields.Float(string='Saldo Facturas Proveedor', digits=(15,2), compute='_set_saldo_provedores')    
    
    acreedores_general         = fields.One2many('account.payment', 'id', string='Acreedores (General)', compute='_set_acreedores_general')    
    acreedores_ids_abonos      = fields.One2many('account.payment', 'id', string='Acreedores (Abonos)', compute='_set_acreedores_abonos')
    saldo_acreedores_abonos    = fields.Float(string='Saldo Acreedores Abonos', digits=(15,2), compute='_set_saldo_acreedores_abonos')    
    acreedores_ids_prestamos   = fields.One2many('account.payment', 'id', string='Acreedores (Préstamos)', compute='_set_acreedores_prestamos')
    saldo_acreedores_prestamos = fields.Float(string='Saldo Acreedores Préstamos', digits=(15,2), compute='_set_saldo_acreedores_prestamos')
    
    saldo = fields.Float(string='Saldo', digits=(15,2), compute='_set_saldo') 



    @api.one
    @api.depends('contacto_id')
    def _set_compania(self):
        self.compania_id = self.env['res.partner'].search([('id', '=', self.contacto_id.id)]).company_id.id



    @api.multi
    @api.depends('contacto_id')
    def _set_facturas_clientes(self):
        for rec in self:
            rec.facturas_clientes_ids = self.env['account.invoice'].search([('state', '=', 'open'),
                                                                            ('type','=','out_invoice'),
                                                                            ('partner_id','=', rec.contacto_id.id)])



    @api.one
    @api.depends('contacto_id')
    def _set_deudores_general(self):
        journal_id_deudores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_deudores %s\n\n', journal_id_deudores)

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'BBVA')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        sql_query = """SELECT id, name, payment_date
                         FROM account_payment 
                        WHERE payment_type = 'transfer' AND
                              x_studio_contacto_deudor_acreedor_1 = self.contacto_id.id AND
                              (journal_id IN journal_id_deudores.ids OR 
                               journal_id IN journal_id_banco.ids) AND
                              (destination_journal_id IN journal_id_banco.ids OR 
                               destination_journal_id IN journal_id_deudores.ids)
                     ORDER BY payment_date;"""
        self.env.cr.execute(sql_query)   
        result = self.env.cr.fetchall()                 
        _logger.info('\n\n\n SUPER QUERY %s\n\n', result)                                   



    @api.one
    @api.depends('contacto_id')
    def _set_deudores_abonos(self):
        journal_id_deudores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_deudores %s\n\n', journal_id_deudores)

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'BBVA')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        abonos = self.env['account.payment'].search([('payment_type', '=', 'transfer'),
                                                     ('x_studio_contacto_deudor_acreedor_1', '=', self.contacto_id.id),
                                                     ('journal_id', 'in', journal_id_deudores.ids),
                                                     ('destination_journal_id', 'in', journal_id_banco.ids)])
        self.deudores_ids_abonos = abonos.ids                                                     



    @api.one
    @api.depends('contacto_id')
    def _set_saldo_deudores_abonos(self):
        self.saldo_deudores_abonos = sum(line.amount * -1 for line in self.deudores_ids_abonos)
        print('abonos_deu',self.saldo_deudores_abonos)



    @api.one
    @api.depends('contacto_id')
    def _set_deudores_prestamos(self):
        journal_id_deudores = self.env['account.journal'].search([('name', 'ilike', 'Deudores diversos')])
        _logger.info('\n journal_id_deudores %s\n\n', journal_id_deudores)

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'BBVA')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        prestamos = self.env['account.payment'].search([('payment_type', '=', 'transfer'),
                                                        ('x_studio_contacto_deudor_acreedor_1', '=', self.contacto_id.id),
                                                        ('journal_id', 'in', journal_id_banco.ids),
                                                        ('destination_journal_id', 'in', journal_id_deudores.ids)])                                                       
        self.deudores_ids_prestamos = prestamos.ids  



    @api.one
    @api.depends('contacto_id')
    def _set_saldo_deudores_prestamos(self):
        self.saldo_deudores_prestamos = sum(line.amount for line in self.deudores_ids_prestamos)
        print('prestamos_deudores',self.saldo_deudores_prestamos)        



    @api.multi
    @api.depends('contacto_id')
    def _set_facturas_proveedores(self):
        for rec in self:
            rec.facturas_proveedores_ids = self.env['account.invoice'].search([('state', '=', 'open'),
                                                                               ('type','=','in_invoice'),
                                                                               ('partner_id','=', rec.contacto_id.id)])


    @api.one
    @api.depends('contacto_id')
    def _set_saldo_provedores(self):
        self.saldo_facturas_proveedores = sum(line.amount_total * -1 for line in self.facturas_proveedores_ids)
        print('self.saldo_facturas_proveedores', self.saldo_facturas_proveedores)



    @api.one
    @api.depends('contacto_id')
    def _set_acreedores_general(self):
        pass



    @api.one
    @api.depends('contacto_id')
    def _set_acreedores_abonos(self):
        journal_id_acreedores = self.env['account.journal'].search([('name', 'ilike', 'Acreedores Diversos')])
        _logger.info('\n journal_id_acreedores %s\n\n', journal_id_acreedores)

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'BBVA')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        abonos = self.env['account.payment'].search([('payment_type', '=', 'transfer'),
                                                     ('x_studio_contacto_deudor_acreedor_1', '=', self.contacto_id.id),
                                                     ('journal_id', 'in', journal_id_banco.ids),
                                                     ('destination_journal_id', 'in', journal_id_acreedores.ids)])                                                                                                          
        self.acreedores_ids_abonos = abonos.ids  



    @api.one
    @api.depends('contacto_id')
    def _set_saldo_acreedores_abonos(self):
        self.saldo_acreedores_abonos = sum(line.amount for line in self.acreedores_ids_abonos)
        print('self.saldo_acreedores_abonos',self.saldo_acreedores_abonos)



    @api.one
    @api.depends('contacto_id')
    def _set_acreedores_prestamos(self):
        journal_id_acreedores = self.env['account.journal'].search([('name', 'ilike', 'Acreedores Diversos')])
        _logger.info('\n journal_id_acreedores %s\n\n', journal_id_acreedores)

        journal_id_banco = self.env['account.journal'].search([('name', 'ilike', 'BBVA')])                                                                
        _logger.info('\n journal_id_banco %s\n\n', journal_id_banco)

        prestamos = self.env['account.payment'].search([('payment_type', '=', 'transfer'),
                                                        ('x_studio_contacto_deudor_acreedor_1', '=', self.contacto_id.id),
                                                        ('journal_id', 'in', journal_id_acreedores.ids),
                                                        ('destination_journal_id', 'in', journal_id_banco.ids)])                                                       
        self.acreedores_ids_prestamos = prestamos.ids
        print('acreedores ids',self.acreedores_ids_prestamos) 



    @api.one
    @api.depends('contacto_id')
    def _set_saldo_acreedores_prestamos(self):
        self.saldo_acreedores_prestamos = sum(line.amount * -1 for line in self.acreedores_ids_prestamos)
        print('acreedores ab',self.saldo_acreedores_prestamos)



    @api.one
    @api.depends('contacto_id')
    def _set_saldo(self):

        total = 0.0
        print('total init',total)          

        total += sum(line.amount_total for line in self.facturas_clientes_ids)
        print('total 1',  total) 

        total += sum(line.amount * -1 for line in self.deudores_ids_abonos)
        print('total 2',total)

        total += sum(line.amount for line in self.deudores_ids_prestamos)
        print('total 3',total)                  

        total += sum(line.amount_total * -1 for line in self.facturas_proveedores_ids)
        print('total 4',total)    

        total += sum(line.amount for line in self.acreedores_ids_abonos)
        print('total 5',total)             

        total += sum(line.amount * -1 for line in self.acreedores_ids_prestamos)
        print('total 6',total)
                       
        self.saldo = total        