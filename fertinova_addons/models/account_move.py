from odoo import models, fields, api
from odoo.osv import expression

class AccountMove(models.Model):
    _inherit = 'account.move'

    prov = fields.Boolean(string="Provisional")
    parent_id = fields.Many2one('account.move', string="Parent")
    inverse_ids = fields.One2many('account.move', 'parent_id')

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
                        'debit' : line.credit,
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
                        'credit' : line.debit,
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
                'line_ids' : array_lines,
                'parent_id': self.id
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

    def update_move(self):
        for line in self.line_ids:
            if line.purchase:
                line.po_status = line.purchase.invoice_status
                if line.purchase.invoice_ids:
                    line.po_date = line.purchase.invoice_ids[0].date_invoice
            elif line.sale:
                line.so_status = line.sale.invoice_status
                if line.sale.invoice_ids:
                    line.so_date = line.sale.invoice_ids[0].date_invoice


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
            self.debit = self.purchase.amount_untaxed
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
            self.debit = False
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
            self.credit = self.sale.amount_untaxed
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
                self.analytic_account_id = self.sale.analytic_account_id
                self.analytic_tag_ids = self.sale.order_line[n_account].analytic_tag_ids
        else:
            self.account_id = False
            self.so_status = False
            self.so_date = False
            self.debit = False
            self.credit = False
            self.partner_id = False
            self.analytic_account_id = False
            self.analytic_tag_ids = False

    
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_invoiced_own(self):
        """
        Compute the invoice status of a SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also the default value if the conditions of no other status is met.
        - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
        - invoiced: if all SO lines are invoiced, the SO is invoiced.
        - upselling: if all SO lines are invoiced or upselling, the status is upselling.

        The invoice_ids are obtained thanks to the invoice lines of the SO lines, and we also search
        for possible refunds created directly from existing invoices. This is necessary since such a
        refund is not directly linked to the SO.
        """
        # Ignore the status of the deposit product
        deposit_product_id = self.env['sale.advance.payment.inv']._default_product_id()
        line_invoice_status_all = [(d['order_id'][0], d['invoice_status']) for d in self.env['sale.order.line'].read_group([('order_id', 'in', self.ids), ('product_id', '!=', deposit_product_id.id)], ['order_id', 'invoice_status'], ['order_id', 'invoice_status'], lazy=False)]
        for order in self:
            invoice_ids = order.order_line.mapped('invoice_lines').mapped('invoice_id').filtered(lambda r: r.type in ['out_invoice', 'out_refund'])
            # Search for invoices which have been 'cancelled' (filter_refund = 'modify' in
            # 'account.invoice.refund')
            # use like as origin may contains multiple references (e.g. 'SO01, SO02')
            refunds = invoice_ids.search([('origin', 'like', order.name), ('company_id', '=', order.company_id.id), ('type', 'in', ('out_invoice', 'out_refund'))])
            invoice_ids |= refunds.filtered(lambda r: order.name in [origin.strip() for origin in r.origin.split(',')])

            # Search for refunds as well
            domain_inv = expression.OR([
                ['&', ('origin', '=', inv.number), ('journal_id', '=', inv.journal_id.id)]
                for inv in invoice_ids if inv.number
            ])
            if domain_inv:
                refund_ids = self.env['account.invoice'].search(expression.AND([
                    ['&', ('type', '=', 'out_refund'), ('origin', '!=', False)], 
                    domain_inv
                ]))
            else:
                refund_ids = self.env['account.invoice'].browse()

            line_invoice_status = [d[1] for d in line_invoice_status_all if d[0] == order.id]

            if order.state not in ('sale', 'done'):
                invoice_status = 'no'
            elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                invoice_status = 'to invoice'
            elif line_invoice_status and all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                invoice_status = 'invoiced'
            elif line_invoice_status and all(invoice_status in ['invoiced', 'upselling'] for invoice_status in line_invoice_status):
                invoice_status = 'upselling'
            else:
                invoice_status = 'no'

            order.update({
                'invoice_count': len(set(invoice_ids.ids + refund_ids.ids)),
                'invoice_ids': invoice_ids.ids + refund_ids.ids,
                'invoice_status': invoice_status
            })