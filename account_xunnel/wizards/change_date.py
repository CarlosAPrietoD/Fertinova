
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WizardChageDate(models.TransientModel):
    _name = 'wizard.change.date'
    _description = 'Change the sync date from an online account'

    sync_date = fields.Date()

    @api.multi
    def change_sync_date(self):
        active_id = self._context.get('active_id')
        journal = self.env['account.journal'].browse(active_id)
        online = journal.bank_statements_source == 'online_sync'
        online_journal = journal.account_online_journal_id
        if not online or not online_journal:
            message = _(("The journal is not correctly configurated. Please"
                         " check that the bank feed is set to 'Automated"
                         " Bank Synchronization' and an online acount is "
                         " configurated for this journal."))
            raise ValidationError(message)
        online_journal.sudo().last_sync = self.sync_date
