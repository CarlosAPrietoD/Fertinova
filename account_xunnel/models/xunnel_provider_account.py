# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class XunnelProviderAccount(models.Model):
    _inherit = 'account.online.provider'

    provider_type = fields.Selection(selection_add=[('xunnel', 'Xunnel')])

    @api.multi
    def sync_journals(self):
        """Get all journals and check them in the database
        to create them if they're not.
        """
        for journal in self._get_journals():
            online_journal = self.env['account.online.journal'].search([
                ('account_online_provider_id', '=', self.id),
                ('online_identifier', '=', journal.get('id_account'))])
            vals = {
                'name': journal.get('name'),
                'balance': journal.get('balance'),
                'account_number': journal.get('number'),
                'online_identifier': journal.get('id_account'),
                'account_online_provider_id': self.id
            }
            if online_journal:
                online_journal.write(vals)
                if online_journal.journal_ids:
                    # previous check to avoid unnecesary requests
                    online_journal.retrieve_transactions()
            else:
                online_journal.create(vals)

    @api.multi
    def _get_journals(self):
        """Requests https://wwww.xunnel.com/ to retrive all journals
        related to the indicated provider.
        """
        res = self.company_id._xunnel(
            'get_xunnel_journals',
            dict(account_identifier=self.provider_account_identifier))
        err = res.get('error')
        if err:
            raise UserError(err)
        return res.get('response')

    @api.multi
    def update_credentials(self):
        raise UserError(_(
            'Updating credentials is not allowed here. '
            'Please go to https://www.xunnel.com/ to achieve that.'))
