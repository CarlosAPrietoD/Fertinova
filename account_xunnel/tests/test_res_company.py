# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import os
from json import dumps, loads

from odoo.tests.common import TransactionCase
from odoo.tools import misc
from requests_mock import mock

from . import response


class TestXunnelAccount(TransactionCase):

    def setUp(self):
        super(TestXunnelAccount, self).setUp()
        self.url = "https://ci.xunnel.com/"
        self.company = self.env['res.company'].browse(
            self.ref('base.main_company'))

    @mock()
    def test_01_sync_xunnel_providers(self, request=None):
        """Test requesting all providers and journals from an user.
        Two providers and 9 providers are returned but one of each is
        already in the database and must not be overwritten.
        """
        def _response(request, context):
            data = loads(request.text)
            path = 'response_journal_%s.json'
            if data.get('account_identifier') == '5ad79e9d0b212a5b608b459a':
                return misc.file_open(os.path.join(
                    'account_xunnel', 'tests', path % '2')).read()
            return misc.file_open(
                os.path.join('account_xunnel', 'tests', path % '1')).read()

        request.post(
            '%sget_xunnel_providers' % self.url,
            text=dumps(dict(
                response=response.PROVIDERS)))
        request.post(
            '%sget_xunnel_journals' % self.url,
            text=_response)
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(
                {'response': '{"balance": 1099, "transactions": []}'}))

        old_providers = len(self.env['account.online.provider'].search([]))
        old_journals = len(self.env['account.online.journal'].search([]))
        self.company._sync_xunnel_providers()
        new_providers = len(self.env['account.online.provider'].search([]))
        new_journals = len(self.env['account.online.journal'].search([]))
        self.assertEquals(new_providers - old_providers, 1)
        self.assertEquals(new_journals - old_journals, 8)
