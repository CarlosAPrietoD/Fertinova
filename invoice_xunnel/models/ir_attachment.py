# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import logging
import json

from lxml import objectify
from odoo import api, models, fields
from datetime import datetime

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    just_downloaded = fields.Boolean(
        compute="_compute_just_downloaded",
        search="_search_just_downloaded", store=False,
        help="""Used to identify the just donwloaded attachments.
 To evaluate if an attachment was just downloaded, we need to
 check the current context.""")

    def _compute_just_downloaded(self):
        downloaded_ids = self._context.get('downloaded_invoice', [])
        for rec in self:
            rec.just_downloaded = rec.id in downloaded_ids

    def _search_just_downloaded(self, operator, value):
        operator = 'in' if value else 'not int'
        return [('id', operator, self._context.get('downloaded_invoice', []))]

    @api.model
    def create(self, values):
        if 'datas' in values and self._validate_xml(values['datas']):
            description = self._create_description(values['datas'])
            values.update(description)
        return super().create(values)

    @api.multi
    def write(self, values):
        no_mx_rec = self
        for rec in self:
            datas = values['datas'] if 'datas' in values else rec.datas
            if (('description' in values or 'datas' in values) and
                    self._validate_xml(datas)):
                description = self._create_description(datas)
                rec_values = values.copy()
                rec_values.update(description)
                super(IrAttachment, rec).write(rec_values)
                no_mx_rec -= rec
            elif ('datas' in values and rec.mimetype == 'application/xml' and
                    not self._validate_xml(datas)):
                rec_values = values.copy()
                rec_values.update({
                    'description': False,
                    'mimetype': self._compute_mimetype({'datas': datas})
                })
                super(IrAttachment, rec).write(rec_values)
                no_mx_rec -= rec
        return super(IrAttachment, no_mx_rec).write(values)

    @api.model
    def _validate_xml(self, datas):
        if not datas:
            return False
        data_file = base64.b64decode(datas)
        try:
            objectify.fromstring(data_file)
        except (SyntaxError, ValueError):
            return False
        return True

    @api.model
    def _create_description(self, datas):
        """Process XML file to get description.
        Args:
            datas (binary): attachment in base64.
        Returns:
            dict: procesed description dict or empty dict.
        """
        xml_str = base64.b64decode(datas)
        try:
            xml_obj = objectify.fromstring(xml_str)
        except (SyntaxError, ValueError) as err:
            _logger.error(str(err))
            return {}
        if (xml_obj.get('Version') != '3.3' or
                xml_obj.get('TipoDeComprobante') != 'I'):
            return {}
        partner = self.env['res.partner'].search([
            ('vat', '=ilike', xml_obj.Emisor.get('Rfc'))], limit=1)
        if not partner:
            wizard_attachment = self.env['xunnel.attach.xmls.wizard']
            wizard_attachment.create_partner(datas, '')
        return {
            'description': json.dumps(
                self._prepare_description_attachment(xml_obj),
                ensure_ascii=False),
            'mimetype': 'application/xml',
        }

    @api.model
    def _prepare_description_attachment(self, xml):
        # TODO: Check if we can avoid use enterprise.
        cfdi = self.env['account.invoice'].l10n_mx_edi_get_tfd_etree(xml)
        data = {
            'date': xml.get('Fecha', ' ').replace('T', ' '),
            'number': xml.get('Folio', ''),
            'name': xml.Emisor.get('Nombre', ' '),
            'emitter_vat': xml.Emisor.get('Rfc', ' '),
            'subtotal': float(xml.get('SubTotal', '0.0')),
            'tax': 0.0,
            'tax_retention': 0.0,
            'currency': xml.get('Moneda', ''),
            'total': float(xml.get('Total')),
            'uuid': cfdi.get('UUID') if cfdi is not None else ' ',
        }
        if hasattr(xml, 'Impuestos'):
            data.update({
                'tax': float(xml.Impuestos.get(
                    'TotalImpuestosTrasladados', '0.0')),
                'tax_retention': float(xml.Impuestos.get(
                    'TotalImpuestosRetenidos', '0.0')),
            })
        return data

    emitter_partner_id = fields.Many2one(
        'res.partner',
        compute="_compute_emitter_partner_id",
        string="Emitter",
        help="In case this is a CFDI file, stores emitter's name.",
        store=True)
    xunnel_attachment = fields.Boolean(
        help="Specify if this is a XUNNEL attachment.")
    invoice_total_amount = fields.Float(
        string='Total Amount',
        compute="_compute_emitter_partner_id",
        help="In case this is a CFDI file, stores invoice's total amount.",
        store=True)
    stamp_date = fields.Datetime(
        compute="_compute_emitter_partner_id",
        help="In case this is a CFDI file, stores invoice's stamp date.",
        store=True)
    product_list = fields.Text(
        compute="_compute_emitter_partner_id",
        string='Products',
        help="In case this is a CFDI file, show invoice's product list",
    )
    related_cfdi = fields.Text(
        compute="_compute_emitter_partner_id",
        string='Related CFDI',
        help="Related CFDI of the XML file",
    )

    @api.multi
    @api.depends('datas')
    def _compute_emitter_partner_id(self):
        attachments = self.filtered(
            lambda rec: rec.xunnel_attachment and rec.datas_fname and
            rec.datas_fname.lower().endswith('xml'))
        for rec in attachments:
            xml = rec.get_xml_object(rec.datas)
            if xml is None:
                return
            rfc = xml.Emisor.get('Rfc', '').upper()
            partner = self.env['res.partner'].search([
                ('vat', '=', rfc), '|',
                ('supplier', '=', True), ('customer', '=', True)
            ], limit=1)
            stamp_date = xml.Complemento.xpath(
                'tfd:TimbreFiscalDigital[1]',
                namespaces={
                    'tfd':
                    'http://www.sat.gob.mx/TimbreFiscalDigital'})[0].get(
                        'FechaTimbrado')

            rec.emitter_partner_id = partner.id
            rec.invoice_total_amount = xml.get('Total')
            rec.stamp_date = datetime.strptime(stamp_date, "%Y-%m-%dT%H:%M:%S")
            product_list = []
            for concepto in xml.Conceptos.iter(
                    '{http://www.sat.gob.mx/cfd/3}Concepto'):
                product_list.append(concepto.get('Descripcion'))
            rec.product_list = json.dumps(product_list)
            try:
                related_uuid = []
                for related in xml.CfdiRelacionados.iter(
                        '{http://www.sat.gob.mx/cfd/3}CfdiRelacionado'):
                    related_uuid.append(related.get('UUID'))
                    rec.related_cfdi = json.dumps(related_uuid)
            except AttributeError:
                rec.related_cfdi = None

    @api.multi
    def get_xml_object(self, xml):
        try:
            if isinstance(xml, bytes):
                xml = xml.decode()
            xml_str = base64.b64decode(xml.replace(
                'data:text/xml;base64,', ''))
            xml = objectify.fromstring(xml_str)
        except (AttributeError, SyntaxError):
            xml = None
        return xml
