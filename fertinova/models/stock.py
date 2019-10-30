# Copyright 2019 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    accounting_date = fields.Date(
        help="Date at which the accounting entries will be created"
        " in case of automated product in picking.",
        default=fields.Date.today)

    @api.multi
    def action_done(self):
        """Inherit method to add for context the accounting_date in the
        account_entry"""
        for picking in self:
            res = super(Picking, picking.with_context(
                force_period_date=picking.accounting_date)).action_done()
        return res
