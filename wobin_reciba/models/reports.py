from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class QualityAvgHumidity(models.TransientModel):    
    _name='quality.avg.humidity'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportAvgHumidity(models.AbstractModel):
    #Reporte promedio ponderado de humedad
    _name = 'report.wobin_reciba.report_avg_humidity'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['quality.avg.humidity'].browse(docids)
        tickets_receipt = self.env['reciba.ticket'].search([('operation_type','=','in'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('destination_id','=',report.location.id),'|',('state','=','priceless'),('state','=','confirmed')])
        tickets_delivery = self.env['reciba.ticket'].search([('operation_type','=','out'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('origin_id','=',report.location.id),('state','=','confirmed')])    
        sum_net_receipt = 0
        sum_humidity_receipt = 0
        avg_humidity_receipt = 0
        sum_net_delivery = 0
        sum_humidity_delivery = 0
        avg_humidity_delivery = 0
        for receipt in tickets_receipt:
            sum_net_receipt += receipt.net_weight
            sum_humidity_receipt += receipt.net_weight * receipt.humidity
        avg_humidity_receipt = sum_humidity_receipt/sum_net_receipt
        for delivery in tickets_delivery:
            sum_net_delivery += delivery.net_weight
            sum_humidity_delivery += delivery.net_weight * delivery.humidity
        avg_humidity_delivery = sum_humidity_delivery/sum_net_delivery
        dif_net = sum_net_receipt - sum_net_delivery
        dif_avg = avg_humidity_receipt - avg_humidity_delivery
        tolerance = sum_net_receipt * dif_avg
        decrease = dif_net - tolerance

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net_receipt' : sum_net_receipt,
            'sum_humidity_receipt' : sum_humidity_receipt,
            'avg_humidity_receipt' : avg_humidity_receipt,
            'sum_net_delivery' : sum_net_delivery,
            'sum_humidity_delivery' : sum_humidity_delivery,
            'avg_humidity_delivery' : avg_humidity_delivery,
            'dif_net' : dif_net,
            'dif_avg' : dif_avg,
            'tolerance' : tolerance,
            'decrease' : decrease,
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : tickets_receipt,
            'deliveries' : tickets_delivery,
        }