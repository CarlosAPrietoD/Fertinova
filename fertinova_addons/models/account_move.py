from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    prov = fields.Boolean(string="Provisional")

    def duplicate_account(self, context=None):
        
        array_lines = []

        for line in self.line_ids:
            if line.purchase and line.po_status and line.po_date:
                if line.po_status == 'paid':
                    tag_lines = []
                    for tag in line.analytic_tag_ids:
                        tag_lines.append((4,tag.id))
                    line_vals = {
                            'purchase': line.purchase.id,
                            'po_status' : line.po_status,
                            'po_date' : line.po_date,
                            'account_id' : line.account_id.id,
                            'debit' : line.credit,
                            'partner_id' : line.partner_id.id,
                            'analytic_account_id' : line.analytic_account_id.id,
                            'analytic_tag_ids' : tag_lines
                            }

                    array_lines.append((0,0,line_vals))
            
            if line.sale and line.so_status and line.so_date:
                if line.so_status == 'paid':
                    tag_lines = []
                    for tag in line.analytic_tag_ids:
                        tag_lines.append((4,tag.id))
                    line_vals = {
                            'sale': line.sale.id,
                            'so_status' : line.so_status,
                            'so_date' : line.so_date,
                            'account_id' : line.account_id.id,
                            'credit' : line.debit,
                            'partner_id' : line.partner_id.id,
                            'analytic_account_id' : line.analytic_account_id.id,
                            'analytic_tag_ids' : tag_lines
                            }

                    array_lines.append((0,0,line_vals))
        
        vals = {
                'ref': self.ref,
                'journal_id' : self.journal_id.id,
                'line_ids' : array_lines
                }
        new_move = self.env['account.move'].create(vals)

        return {
                'view_type' : 'form',
                'view_mode' : 'form',
                'res_id': new_move.id,
                'res_model' : 'account.move',
                'type' : 'ir.actions.act_window',
                'target' : 'current',
                }

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase = fields.Many2one('purchase.order', string="Purchase Order")
    po_status = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ],string="PO invoice status")
    po_date = fields.Date(string="PO invoice date")
    sale = fields.Many2one('sale.order', string="Sale Order")
    so_status = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ],string="SO invoice status")
    so_date = fields.Date(string="SO invoice date")

    @api.multi
    @api.onchange('purchase')
    def get_account_po(self):
        if self.purchase:
            if self.purchase.invoice_ids:
                self.account_id = self.purchase.invoice_ids[0].invoice_line_ids[0].account_id
                self.po_status = self.purchase.invoice_ids[0].state
                self.po_date = self.purchase.invoice_ids[0].date_invoice
                self.credit = self.purchase.invoice_ids[0].amount_total
                self.partner_id = self.purchase.invoice_ids[0].partner_id
                self.analytic_account_id = self.purchase.invoice_ids[0].invoice_line_ids[0].account_analytic_id
                self.analytic_tag_ids = self.purchase.invoice_ids[0].invoice_line_ids[0].analytic_tag_ids
            else:
                self.account_id = False
                self.po_status = False
                self.po_date = False
                self.credit = False
                self.partner_id = False
                self.analytic_account_id = False
                self.analytic_tag_ids = False
        else:
            self.account_id = False
            self.po_status = False
            self.po_date = False
            self.credit = False
            self.partner_id = False
            self.analytic_account_id = False
            self.analytic_tag_ids = False

    
    @api.multi
    @api.onchange('sale')
    def get_account_so(self):
        if self.sale:
            if self.sale.invoice_ids:
                self.account_id = self.sale.invoice_ids[0].invoice_line_ids[0].account_id
                self.so_status = self.sale.invoice_ids[0].state
                self.so_date = self.sale.invoice_ids[0].date_invoice
                self.debit = self.sale.invoice_ids[0].amount_total
                self.partner_id = self.sale.invoice_ids[0].partner_id
                self.analytic_account_id = self.sale.invoice_ids[0].invoice_line_ids[0].account_analytic_id
                self.analytic_tag_ids = self.sale.invoice_ids[0].invoice_line_ids[0].analytic_tag_ids
            else:
                self.account_id = False
                self.so_status = False
                self.so_date = False
                self.debit = False
                self.partner_id = False
                self.analytic_account_id = False
                self.analytic_tag_ids = False
        else:
            self.account_id = False
            self.so_status = False
            self.so_date = False
            self.debit = False
            self.partner_id = False
            self.analytic_account_id = False
            self.analytic_tag_ids = False

    
    