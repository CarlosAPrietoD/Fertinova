# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from json import dumps
from odoo import _, api, fields, models
from odoo.exceptions import UserError
import logging
import requests
from requests.exceptions import HTTPError

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    xunnel_token = fields.Char()
    xunnel_testing = fields.Boolean()

    @api.multi
    def _xunnel(self, endpoint, payload=None):
        """_xunnel calls xunnel.com and returns it response.
            if is there any an exception. The error message within the API
            response will be raised.
        """
        self.ensure_one()
        if not self.xunnel_token:
            raise UserError(_('You need to define Xunnel Token'))
        base = self.env['ir.config_parameter'].sudo().get_param(
            'account_xunnel.xunnel_server_url')
        if self.xunnel_testing:
            base = self.env['ir.config_parameter'].sudo().get_param(
                'account_xunnel.test_xunnel_server_url')
        origin_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        response = requests.post(
            str(base) + endpoint,
            headers={
                'Xunnel-Token': str(self.xunnel_token),
                'Xunnel-Origin': origin_url
            },
            data=dumps(payload) if payload else None)
        try:
            response.raise_for_status()
        except HTTPError as error:
            raise UserError(error)
        return response.json()

    @api.multi
    def _sync_xunnel_providers(self, providers=None):
        """Requests https://wwww.xunnel.com/ to retrive all providers
        related to the current company and check them in the database
        to create them if they're not. After sync journals.
        """
        self.ensure_one()
        params = {}
        if providers:
            params['provider_account_identifier'] = providers
        providers_response = self._xunnel('get_xunnel_providers', params)
        error = providers_response.get('error')
        if error:
            return False, error
        all_providers = providers_response.get('response')
        for provider in all_providers:
            provider.update(company_id=self.id, provider_type='xunnel')
            online_provider = self.env['account.online.provider'].search([
                ('provider_account_identifier', '=',
                 provider.get('provider_account_identifier')),
                ('company_id', '=', self.id)], limit=1)
            if online_provider:
                online_provider.write(provider)
            else:
                online_provider = online_provider.create(provider)
            online_provider.sync_journals()
        return True, all_providers
