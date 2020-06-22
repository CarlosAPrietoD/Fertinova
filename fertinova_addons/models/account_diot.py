# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MxReportPartnerLedger(models.AbstractModel):
    _inherit = "l10n_mx.account.diot"

    @api.model
    def _get_lines(self, options, line_id=None):
        lines = super(MxReportPartnerLedger, self)._get_lines(options)
        for line in lines:
            if line.get('parent_id', False) and not line.get('class', False) and line.get('level') == 1:
                apr_caba = self.env['account.move.line'].browse(int(line.get('id'))).move_id.tax_cash_basis_rec_id
                invoice_aml = apr_caba.credit_move_id | apr_caba.debit_move_id
                invoice_w_cfdi = invoice_aml.mapped('invoice_id').filtered('l10n_mx_edi_cfdi_uuid')
                if invoice_w_cfdi:
                    line['name'] = '%s (%s)' % (line['name'], invoice_w_cfdi[0].l10n_mx_edi_cfdi_uuid)
        return lines
