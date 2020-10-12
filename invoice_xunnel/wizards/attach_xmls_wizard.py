
from odoo import models, api


class AttachXmlsWizard(models.TransientModel):
    _inherit = 'xunnel.attach.xmls.wizard'

    @api.model
    def check_xml(self, files, account_id=False):
        response = super().check_xml(files=files, account_id=account_id)
        if not self.env.context.get('autofill_enable'):
            return response
        attachment_obj = self.env['ir.attachment']
        invoice_obj = self.env['account.invoice']
        invoice_tag = self.env.ref('invoice_xunnel.with_invoice')
        no_invoice_tag = self.env.ref('invoice_xunnel.without_invoice')
        invoice_files = response.get('invoices')
        for invoice_file in invoice_files:
            invoice_data = invoice_files[invoice_file]
            invoice_id = invoice_data.get('invoice_id', False)
            invoice = invoice_obj.browse(invoice_id)
            attachment = attachment_obj.search(
                [('name', '=', invoice_file)], limit=1)
            if not attachment:
                continue
            attachment.write({
                'tag_ids': [(3, no_invoice_tag.id, None), (4, invoice_tag.id)],
                'res_id': invoice.id,
                'res_model': 'account.invoice',
            })
        return response
