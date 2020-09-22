# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests.common import TransactionCase
from requests_mock import mock
from json import dumps
from . import response


class TestXunnelAccount(TransactionCase):

    def setUp(self):
        super(TestXunnelAccount, self).setUp()
        self.url = "https://ci.xunnel.com/"
        self.journal = self.env.ref(
            'account_xunnel.account_journal_attachments')

    @mock()
    def test_01_retrieve_transactions_last_sync(self, request):
        """Test requesting all transactions from an account and
        how many bank statement were created. Also checks last_sync's refreshed
        """
        self.env['account.bank.statement'].search([
            ('journal_id', '=', self.journal.id)]).unlink()
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(dict(response=dumps({
                'balance': 0,
                'transactions': response.TRANSACTIONS}))))
        online_journal = self.journal.account_online_journal_id
        transactions = self.journal.manual_sync()
        self.assertNotEquals(online_journal.last_sync, False)
        self.assertEquals(transactions, 7)

    @mock()
    def test_02_bad_retrieve_transactions_last_sync(self, request):
        """Test making a bank statement form online journal without
        having assigned an account journal. Also checks last_sync's refreshed
        """
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(dict(response=dumps({
                'balance': 0,
                'transactions': response.TRANSACTIONS}))))
        online_journal = self.journal.account_online_journal_id
        # To test if manual_sync its executed before is assigned to a journal
        online_journal.last_sync = False
        online_journal.journal_ids = False
        statements = online_journal.retrieve_transactions()
        self.assertFalse(online_journal.last_sync)
        self.assertEquals(statements, 0)

    @mock()
    def test_03_link_manual_transactions(self, request):
        """Test to validate if you create statement lines manually, it should
        update that entries to link it with the one updated from xunnel.
        """
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(dict(response=dumps({
                'balance': 0,
                'transactions': response.TRANSACTIONS}))))
        self.journal.bank_statement_creation = 'month'
        statement = self.env['account.bank.statement'].create({
            'name': 'online sync',
            'line_ids': [(0, 0, {
                'name': 'Transaction 1',
                'date': '2014-10-05',
                'amount': 10,
            })],
            'date': '2014-10-05',
            'journal_id': self.journal.id,
        })
        line = statement.line_ids
        self.assertFalse(line.online_identifier)
        self.journal.manual_sync()
        self.assertEquals(
            line.online_identifier, '5a9dcb3d244283f35a8c6e26')

    @mock()
    def test_04_duplicate_manual_transactions(self, request):
        """Test to validate if you create more than one equal statement line
        manually, it should let that records an create new transactions.
        """
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(dict(response=dumps({
                'balance': 0,
                'transactions': response.TRANSACTIONS}))))
        self.journal.bank_statement_creation = 'month'
        statement = self.env['account.bank.statement'].create({
            'name': 'online sync',
            'line_ids': [(0, 0, {
                'name': 'Transaction 1',
                'date': '2014-10-05',
                'amount': 10,
            }), (0, 0, {
                'name': 'Transaction 2',
                'date': '2014-10-05',
                'amount': 10,
            })],
            'date': '2014-10-05',
            'journal_id': self.journal.id,
        })
        self.journal.manual_sync()
        lines = statement.line_ids.filtered(lambda l: not l.online_identifier)
        self.assertEquals(len(lines), 2)
        self.assertNotEquals(len(statement.line_ids), 2)

    @mock()
    def test_05_statements_by_period(self, request):
        """Test to validate the creation of bank statements depending on the
        configuration of of the journal bank_statement_creation field.
        """
        request.post(
            '%sget_xunnel_transactions' % self.url,
            text=dumps(dict(response=dumps({
                'balance': 0,
                'transactions': response.TRANSACTIONS}))))
        month = self.process_statements_by_period('month')
        self.assertEquals(len(month), 2)
        day = self.process_statements_by_period('day')
        self.assertEquals(len(day), 6)
        week = self.process_statements_by_period('week')
        self.assertEquals(len(week), 3)
        bimonthly = self.process_statements_by_period('bimonthly')
        self.assertEquals(len(bimonthly), 3)

    def process_statements_by_period(self, period):
        statement_obj = self.env['account.bank.statement']
        statement_obj.search([('journal_id', '=', self.journal.id)]).unlink()
        self.journal.bank_statement_creation = period
        self.journal.manual_sync()
        return statement_obj.search([('journal_id', '=', self.journal.id)])
