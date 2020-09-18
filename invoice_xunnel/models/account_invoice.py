# Copyright 2017, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from codecs import BOM_UTF8

from odoo import _, api, models

BOM_UTF8U = BOM_UTF8.decode('UTF-8')
CFDI_SAT_QR_STATE = {
    'No Encontrado': 'not_found',
    'Cancelado': 'cancelled',
    'Vigente': 'valid',
}


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def generate_xml_attachment(self):
        self.ensure_one()
        if not self.l10n_mx_edi_cfdi:
            return False
        fname = ("%s-%s-MX-Bill-%s.xml" % (
            self.journal_id.code, self.reference,
            self.company_id.partner_id.vat or '')).replace('/', '')
        data_attach = {
            'name': fname,
            'datas': base64.encodebytes(
                self.l10n_mx_edi_cfdi and
                self.l10n_mx_edi_cfdi.lstrip(BOM_UTF8U).encode('UTF-8') or ''),
            'datas_fname': fname,
            'description': _('XML signed from Invoice %s.') % self.number,
            'res_model': self._name,
            'res_id': self.id,
        }
        self.l10n_mx_edi_cfdi_name = fname
        return self.env['ir.attachment'].with_context({}).create(data_attach)

    @api.multi
    def create_adjustment_line(self, xml_amount):
        """If the invoice has difference with the total in the CFDI is
        generated a new line with that adjustment if is found the account to
        assign in this lines. The account is assigned in a system parameter
        called 'adjustment_line_account_MX'"""
        account_id = self.env['ir.config_parameter'].sudo().get_param(
            'adjustment_line_account_MX', '')
        if not account_id:
            return False
        self.invoice_line_ids.create({
            'account_id': account_id,
            'name': _('Adjustment line'),
            'quantity': 1,
            'price_unit': xml_amount - self.amount_total,
            'invoice_id': self.id,
        })
        return True
