# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #///////////////////////////////
    #  Fields to add
    #///////////////////////////////
    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')
    
    #is_waste   = fields.Boolean(string='¿Es merma?')
    is_surplus = fields.Boolean(string='¿Es excedente?')
 -*- coding: utf-8 -*-
2
from collections import defaultdict
3
from odoo import models, fields, api
4
​
5
​
6
class StockPicking(models.Model):
7
    _inherit = 'stock.picking'
8
​
9
    #///////////////////////////////
10
    #  Fields to add
11
    #///////////////////////////////
12
    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')
13
    
14
    #is_waste   = fields.Boolean(string='¿Es merma?')
15
    is_surplus = fields.Boolean(string='¿Es excedente?')
16
​
17
    waste_ids  = fields.Many2many('stock.scrap', string='Folio Desecho', compute='_set_waste_ids')
18
    surplus_id = fields.Many2one('stock.picking', string='Folio Excedente', compute='_set_surplus_id')
19
​
20
    delivery_amount  = fields.Float(string='Entrega', digits=(20, 2), compute='_set_delivery_amount')
21
    waste_amount     = fields.Float(string='Desecho', digits=(20, 2), compute='_set_waste_amount')
22
    surplus_amount   = fields.Float(string='Excedente', digits=(20, 2), compute='_set_surplus_amount')
23
    eff_qty_amount   = fields.Float(string='Cantidad Efectivamente Recibida', digits=(20, 2), compute='_set_eff_qty_amount')
24
    d_eff_qty_amount = fields.Float(string='Cantidad Efectivamente Entregada', digits=(20, 2), compute='_set_d_eff_qty_amount'
25
​
26
    custom_partner_id  = fields.Many2one('res.partner', string='Cliente', compute='_set_partner')
27
    custom_date_order  = fields.Datetime(string='Fecha', compute='_set_date_order')
28
    custom_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm', compute='_set_incoterm')
29
​
30
​
31
​
32
    @api.one 
33
    def _set_waste_ids(self):
34
        self.waste_ids = self.env['stock.scrap'].search([('picking_id', '=', self.id)]).ids         
35
​
36
​
37
​
38
    @api.one 
39
    def _set_surplus_id(self):
40
        self.surplus_id = self.env['stock.picking'].search([('is_surplus', '=', True),
41
                                                            ('origin_transfer_id', '=', self.id)], limit=1).id 
42
​
43
​
44
​
45
    @api.one
46
    @api.depends('name')
47
    def _set_delivery_amount(self):
48
        self.delivery_amount = sum(line.quantity_done for line in self.move_ids_without_package)                                                                    
49
​
50
​
51
​
52
    @api.one
53
    @api.depends('waste_ids')
54
    def _set_waste_amount(self):
55
        waste_objs = self.env['stock.scrap'].search([('picking_id', '=', self.id)])
56
        self.waste_amount = sum(rec.scrap_qty for rec in waste_objs)
    waste_ids  = fields.Many2many('stock.scrap', string='Folio Desecho', compute='_set_waste_ids')
    surplus_id = fields.Many2one('stock.picking', string='Folio Excedente', compute='_set_surplus_id')

    delivery_amount  = fields.Float(string='Entrega', digits=(20, 2), compute='_set_delivery_amount')
    waste_amount     = fields.Float(string='Desecho', digits=(20, 2), compute='_set_waste_amount')
    surplus_amount   = fields.Float(string='Excedente', digits=(20, 2), compute='_set_surplus_amount')
    eff_qty_amount   = fields.Float(string='Cantidad Efectivamente Recibida', digits=(20, 2), compute='_set_eff_qty_amount')
    d_eff_qty_amount = fields.Float(string='Cantidad Efectivamente Entregada', digits=(20, 2), compute='_set_d_eff_qty_amount')

    custom_partner_id  = fields.Many2one('res.partner', string='Cliente', compute='_set_partner')
    custom_date_order  = fields.Datetime(string='Fecha', compute='_set_date_order')
    custom_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm', compute='_set_incoterm')



    @api.one 
    def _set_waste_ids(self):
        self.waste_ids = self.env['stock.scrap'].search([('picking_id', '=', self.id)]).ids         



    @api.one 
    def _set_surplus_id(self):
        self.surplus_id = self.env['stock.picking'].search([('is_surplus', '=', True),
                                                            ('origin_transfer_id', '=', self.id)], limit=1).id 



    @api.one
    @api.depends('name')
    def _set_delivery_amount(self):
        self.delivery_amount = sum(line.quantity_done for line in self.move_ids_without_package)                                                                    



    @api.one
    @api.depends('waste_ids')
    def _set_waste_amount(self):
        waste_objs = self.env['stock.scrap'].search([('picking_id', '=', self.id)])
        self.waste_amount = sum(rec.scrap_qty for rec in waste_objs)



    @api.one
    @api.depends('surplus_id')
    def _set_surplus_amount(self):
        self.surplus_amount = sum(line.quantity_done for line in self.surplus_id.move_ids_without_package)



    @api.one
    @api.depends('waste_amount', 'surplus_amount')
    def _set_eff_qty_amount(self):          
        self.eff_qty_amount = self.delivery_amount - self.waste_amount + self.surplus_amount 



    @api.one
    @api.depends('waste_amount', 'surplus_amount')
    def _set_d_eff_qty_amount(self):          
        self.d_eff_qty_amount = self.delivery_amount - self.waste_amount + self.surplus_amount 


    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_partner(self):   
        if self.sale_id:
            self.custom_partner_id = self.env['res.partner'].search([('id', '=', self.sale_id.partner_id.id)]).id
        elif self.purchase_id:       
            self.custom_partner_id = self.env['res.partner'].search([('id', '=', self.purchase_id.partner_id.id)]).id



    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_date_order(self):   
        if self.sale_id:
            self.custom_date_order = self.env['sale.order'].search([('id', '=', self.sale_id.id)]).date_order
        elif self.purchase_id:       
            self.custom_date_order = self.env['purchase.order'].search([('id', '=', self.purchase_id.id)]).date_order           



    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_incoterm(self):   
        if self.sale_id:
            self.custom_incoterm_id = self.env['sale.order'].search([('id', '=', self.sale_id.id)]).incoterm.id
        elif self.purchase_id:       
            self.custom_incoterm_id = self.env['purchase.order'].search([('id', '=', self.purchase_id.id)]).incoterm_id.id




    #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
    #Open a new window for surplus
    @api.multi
    def open_stock_picking_surplus(self):
        #Get current company_id from user where this process will apply just to GRANERO:
        company_aux_id = self.env['res.company'].browse(self.env['res.company']._company_default_get('your.module')).id
        company_id = company_aux_id.id

        #GRANERO is ID '2' in Companies:
        if company_id == 2:        
            line_ids_list    = list()
            item             = tuple()
            dictionary_vals  = dict()

            #Iterate over items in lines of stock picking
            #in order to construct data pre-filled for new
            #window of surplus transfer:
            for line in self.move_ids_without_package:  
                #Construct tuple item for each line (0, 0, dictionary_vals)
                dictionary_vals = {
                    'name': line.name,
                    'state': 'draft',
                    'product_id': line.product_id.id,
                    'date_expected': fields.datetime.now(),
                    'product_uom': line.product_uom.id,
                    'is_locked': False,
                    'show_operations': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)       

            #Fill with this fixed data 
            sequence         = self.env['ir.sequence'].next_by_code('self.surplustock') or 'New'
            name_seq         = sequence             
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 170)]).id 
            location_id      = self.env['stock.location'].search([('name', '=', self.location_id.name)]).id                                                                    

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': name_seq,
                'default_picking_type_id': picking_type,
                'default_location_id': self.location_id.id,
                'default_origin_transfer_id': self.id,
                'default_is_surplus': True,
                'default_surplus_id': self.id,
                'default_move_ids_without_package': line_ids_list
            }

            #Return new window of surplus transfer:
            return {
                #'name':_("Excedentes"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'stock.picking',
                #'res_id': partial_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
                'context': ctxt            
            }     
