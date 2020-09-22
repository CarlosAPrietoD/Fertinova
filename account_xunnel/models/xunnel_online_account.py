# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import json
from datetime import datetime
from time import mktime
from odoo import api, models, _
from odoo.exceptions import UserError


class ProviderAccount(models.Model):
    _inherit = 'account.online.journal'

    @api.multi
    def retrieve_transactions(self, forced_params=None):
        self.ensure_one()
        if self.account_online_provider_id.provider_type != 'xunnel':
            return super(ProviderAccount, self).retrieve_transactions()
        resp_json = self._get_transactions(forced_params)
        transactions = self._prepare_transactions(resp_json)
        if not transactions:
            return 0
        response = self._process_transactions(transactions)
        return response

    @api.multi
    def _get_transactions(self, forced_params):
        params = {
            'id_account': self.online_identifier,
            'id_credential':
                self.account_online_provider_id.provider_account_identifier
        }
        if forced_params is not None:
            params.update(forced_params)
        elif self.last_sync:
            params.update(
                dt_transaction_from=mktime(self.last_sync.timetuple()))
        resp = self.env.user.company_id._xunnel(
            'get_xunnel_transactions', params)
        err = resp.get('error')
        if err:
            raise UserError(err)
        return json.loads(resp.get('response'))

    @api.multi
    def _prepare_transactions(self, resp_json):
        json_transactions = resp_json['transactions']
        if not self.journal_ids or not json_transactions:
            return False
        journal = self.journal_ids[0]
        transactions = {}
        for transaction in json_transactions:
            date = datetime.strptime(
                transaction['dt_authorization'], '%Y-%m-%d')
            trans = {
                'name': transaction['description'],
                'ref': transaction['reference'],
                'online_identifier': transaction['id_transaction'],
                'date': date.date(),
                'amount': transaction['amount'],
                'end_amount': resp_json['balance'],
                'card_number': transaction['card_number'],
            }
            manual_lines = self.env['account.bank.statement.line'].search([
                ('journal_id', '=', journal.id),
                ('date', '=', trans['date']),
                ('amount', '=', trans['amount']),
                ('online_identifier', '=', False)], limit=2)
            if len(manual_lines) == 1:
                manual_lines.online_identifier = trans['online_identifier']
                manual_lines.name += ' - ' + trans['name']
                continue
            if 'meta' in transaction and 'location' in transaction['meta']:
                trans['location'] = transaction['meta']['location']
            if journal.bank_statement_creation == 'day':
                transactions.setdefault(
                    transaction['dt_authorization'], []).append(trans)
            elif journal.bank_statement_creation == 'week':
                week = date.isocalendar()[1]
                transactions.setdefault(week, []).append(trans)
            elif journal.bank_statement_creation == 'bimonthly':
                if date.day > 15:
                    transactions.setdefault(
                        date.strftime('%Y-%m-15'), []).append(trans)
                else:
                    transactions.setdefault(
                        date.strftime('%Y-%m-01'), []).append(trans)
            elif journal.bank_statement_creation == 'month':
                transactions.setdefault(
                    date.strftime('%Y-%m'), []).append(trans)
            else:
                transactions.setdefault('transactions', []).append(trans)
        return transactions

    @api.multi
    def _process_transactions(self, transactions):
        journal = self.journal_ids[0]
        statement_obj = self.env['account.bank.statement']
        line_statement_obj = self.env['account.bank.statement.line']
        response = 0
        for __, trans in sorted(transactions.items()):
            response += statement_obj.online_sync_bank_statement(
                trans, journal)
            statement = statement_obj.search(
                [('journal_id', '=', journal.id)],
                order="id desc", limit=1)
            starting_balance = line_statement_obj.search([
                ('statement_id', '=', statement.id),
                ('online_identifier', '=', False),
                ('name', '=', _(
                    'Opening statement: first synchronization')),
                ], limit=1)
            if starting_balance:
                statement.write({'balance_start': starting_balance.amount})
                starting_balance.unlink()
                response -= 1
            last_date = line_statement_obj.search(
                [('statement_id', '=', statement.id)], limit=1,
                order='date desc').date
            statement.date = last_date
            statement.line_ids.filtered('online_identifier').write({
                'note': _('Transaction synchronized from Xunnel')})
        return response
