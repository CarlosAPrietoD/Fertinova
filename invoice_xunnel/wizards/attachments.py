
from odoo import models, api, fields, _


class AttachmentslsWizard(models.TransientModel):
    _name = 'xunnel.attachments.wizard'
    _description = 'Xunnel attachments sync'

    company_id = fields.Many2one(
        'res.company', required=True,
        default=lambda self: self.env.user.company_id)
    date_from = fields.Date(
        related='company_id.xunnel_last_sync',
        readonly=False)
    message = fields.Char(help="Used to show the synchronization status.")
    no_attachment_action = fields.Boolean(help="Used to toggle the redirect to the attachments.")

    @api.multi
    def synchronize_attachments(self):
        """Synchronize attachments from Xunnel. After it,
        opens a new `xunnel.attachments.wizard` instance with
        the message corresponding to the synchronization status.

        If there was downloaded attachments, it also shows a button
        to redirect to those attachments.
        """
        result = self.company_id._sync_xunnel_attachments()
        failed = result.get('failed')
        created = result.get('created')
        message = _("%s xml have been downloaded.") % len(created)
        if failed:
            message += _(" Also %s files have failed at the conversion.") % failed
        action = self.env.ref('invoice_xunnel.action_product_confirm_wizard').read()[0]
        action['context'] = {
            'default_message': message,
            'default_no_attachment_action': not created,
            'downloaded_invoice': created,
        }
        return action

    @api.multi
    def open_attachments(self):
        """Opens the Documents's dashboard, with the just downloaded
        attachments `ir.filter` active. Also the "Finance" folder is opened
        by default.
        """
        folder_id = self.env.ref('documents.documents_finance_folder')
        action = self.env.ref('documents.document_action').read()[0]
        action['context'] = {
            'defaultFolderId': folder_id.id,
            'search_default_filter_downloaded_xml': True,
            'downloaded_invoice': self._context.get('downloaded_invoice'),
        }
        return action
