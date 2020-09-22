# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request, Controller


class MainController(Controller):

    @http.route(
        '/account_xunnel/xunnel_webhook_connection/',
        type='json', auth='public', csrf=False)
    def webhook_hanlder(self, **kw):
        """Recives a request from https://xunnel.com with new data for
        auto-synchronize. It can either synchronize new transactions from
        an existing account or add new accounts to your providers.
        """
        post = request.jsonrequest
        provider = post.get('provider')
        event = post.get('handle')
        data = post.get('sync_data')

        if event == 'refresh':
            for _, journal_data in data.items():
                online_identifier = journal_data.get('journal')
                if not online_identifier:
                    continue
                journal = request.env['account.online.journal'].sudo().search(
                    [('online_identifier', '=', online_identifier)], limit=1)
                journal.retrieve_transactions(forced_params=journal_data)
        else:
            request.env[
                'res.company'].sudo()._sync_xunnel_providers(provider)
