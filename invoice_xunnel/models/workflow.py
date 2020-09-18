# -*- coding: utf-8 -*-
from odoo import models, fields
from json import dumps


class WorkflowActionRuleAccountInherit(models.Model):
    _inherit = 'documents.workflow.rule'

    create_model = fields.Selection(
        selection_add=[('xunnel.invoice', 'Xunnel Invoice')])

    def create_record(self, attachments=None):
        response = super().create_record(attachments=attachments)
        if self.create_model != 'xunnel.invoice':
            return response
        files = []
        for xml in attachments:
            content = xml.datas.decode() if xml.datas else ''
            files.append({'name': xml.name, 'text': content})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'xunnel.attach.xmls.wizard',
            'target': 'new',
            'views': [[False, 'form']],
            'context': {
                'file_names': dumps(files),
                'autofill_enable': True,
                'l10n_mx_edi_invoice_type': 'in',
            }
        }
