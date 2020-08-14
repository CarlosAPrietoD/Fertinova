from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    prov = fields.Boolean(string="Provisional")

    def duplicate_account(self, context=None):
        
        array_lines = []

        for line in self.line_ids:
            if line.purchase:
                tag_lines = []
                for tag in line.analytic_tag_ids:
                    tag_lines.append((4,tag.id))
                date_inv = False
                if line.purchase.invoice_ids:
                    date_inv=line.purchase.invoice_ids[0].date_invoice
                line_vals = {
                        'purchase': line.purchase.id,
                        'po_status' : line.purchase.invoice_status,
                        'po_date' : date_inv,
                        'account_id' : line.account_id.id,
                        'credit' : line.debit,
                        'partner_id' : line.partner_id.id,
                        'analytic_account_id' : line.analytic_account_id.id,
                        'analytic_tag_ids' : tag_lines
                        }

                array_lines.append((0,0,line_vals))
            
            elif line.sale:
                tag_lines = []
                for tag in line.analytic_tag_ids:
                    tag_lines.append((4,tag.id))
                date_inv = False
                if line.sale.invoice_ids:
                    date_inv=line.sale.invoice_ids[0].date_invoice
                line_vals = {
                        'sale': line.sale.id,
                        'so_status' : line.sale.invoice_status,
                        'so_date' : date_inv,
                        'account_id' : line.account_id.id,
                        'debit' : line.credit,
                        'partner_id' : line.partner_id.id,
                        'analytic_account_id' : line.analytic_account_id.id,
                        'analytic_tag_ids' : tag_lines
                        }

                array_lines.append((0,0,line_vals))
            else:
                tag_lines = []
                for tag in line.analytic_tag_ids:
                    tag_lines.append((4,tag.id))
                
                line_vals = {
                        'account_id' : line.account_id.id,
                        'debit' : line.credit,
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
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'No Bill to Receive'),
    ],string="PO invoice status")
    po_date = fields.Date(string="PO invoice date")
    sale = fields.Many2one('sale.order', string="Sale Order")
    so_status = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'No Bill to Receive'),
        ('upselling', 'Upselling Opportunity')
    ],string="SO invoice status")
    so_date = fields.Date(string="SO invoice date")
    prov = fields.Boolean(related='move_id.prov')

    @api.multi
    @api.onchange('purchase')
    def get_account_po(self):
        if self.purchase:
            if self.purchase.invoice_ids:
                self.po_date = self.purchase.invoice_ids[0].date_invoice
            else:
                self.po_date = False
            self.po_status = self.purchase.invoice_status
            self.debit = self.purchase.amount_total
            self.partner_id = self.purchase.partner_id
            n_account=-1
            if self.purchase.order_line:
                n_line=-1
                for line in self.purchase.order_line:
                    n_line+=1
                    if line.product_id:
                        n_account=n_line
            if n_account != -1:
                self.account_id = self.purchase.order_line[n_account].product_id.categ_id.property_account_expense_categ_id
                self.analytic_account_id = self.purchase.order_line[n_account].account_analytic_id
                self.analytic_tag_ids = self.purchase.order_line[n_account].analytic_tag_ids
           
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
                self.so_date = self.sale.invoice_ids[0].date_invoice
            else:
                self.so_date = False
            self.so_status = self.sale.invoice_status
            self.credit = self.sale.amount_total
            self.partner_id = self.sale.partner_id
            n_account=-1
            if self.sale.order_line:
                n_line=-1
                for line in self.sale.order_line:
                    n_line+=1
                    if line.product_id:
                        n_account=n_line
            if n_account != -1:
                self.account_id = self.sale.order_line[n_account].product_id.categ_id.property_account_income_categ_id
                #self.analytic_account_id = self.sale.order_line[n_account].account_analytic_id
                self.analytic_tag_ids = self.sale.order_line[n_account].analytic_tag_ids
        else:
            self.account_id = False
            self.so_status = False
            self.so_date = False
            self.debit = False
            self.partner_id = False
            self.analytic_account_id = False
            self.analytic_tag_ids = False

    
    