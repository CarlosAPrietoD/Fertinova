# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models, fields


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    def _compute_has_synchronized_xunnel(self):
        for rec in self:
            statement = self.env['account.bank.statement'].search(
                [('journal_id', '=', rec.id)],
                order="date desc, id desc", limit=1)
            has_online_sync = statement and self.env[
                'account.bank.statement.line'].search([
                    ('statement_id', '=', statement.id),
                    ('online_identifier', '!=', False)], limit=1)
            is_online_bank = rec.bank_statements_source == 'online_sync'
            rec.has_synchronized_xunnel = (
                is_online_bank and has_online_sync)

    has_synchronized_xunnel = fields.Boolean(
        help='Recognize if has synchronized with Xunnel',
        compute='_compute_has_synchronized_xunnel')
    online_journal_last_sync = fields.Date(
        "Online account last synchronization",
        related="account_online_journal_id.last_sync",
        track_visibility='always')

    @api.multi
    def manual_sync(self):
        online_journal = self.account_online_journal_id
        if online_journal.account_online_provider_id.provider_type != 'xunnel':
            return super(AccountJournal, self).manual_sync()
        return online_journal.retrieve_transactions()
