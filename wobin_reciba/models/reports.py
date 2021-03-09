from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class ReceiptUninvoiced(models.TransientModel):
    #Recepciones por facturar    
    _name='receipt.uninvoiced'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportReceiptUninvoiced(models.AbstractModel):
    #Reporte recepciones por facturar
    _name = 'report.wobin_reciba.report_receipt_uninvoiced'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['receipt.uninvoiced'].browse(docids)
        tickets_uninvoiced = self.env['reciba.ticket'].search([('operation_type','=','in'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('destination_id','=',report.location.id),('invoice_id','=',False),'|',('state','=','priceless'),('state','=','confirmed')])
        
        sum_net = 0
        count = 0
        for receipt in tickets_uninvoiced:
            sum_net += receipt.net_weight
            count += 1
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net' : sum_net,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : tickets_uninvoiced
        }

class ReceiptInvoiced(models.TransientModel):
    #Recepciones facturadas    
    _name='receipt.invoiced'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportReceiptInvoiced(models.AbstractModel):
    #Reporte recepciones facturadas
    _name = 'report.wobin_reciba.report_receipt_invoiced'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['receipt.invoiced'].browse(docids)
        tickets_invoiced = self.env['reciba.ticket'].search([('operation_type','=','in'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('destination_id','=',report.location.id),('invoice_id','!=',False),('state','=','confirmed')])
        
        sum_net = 0
        count = 0
        for receipt in tickets_invoiced:
            sum_net += receipt.net_weight
            count += 1
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net' : sum_net,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : tickets_invoiced
        }

class ReceiptPriceless(models.TransientModel):
    #Recepciones a deposito    
    _name='receipt.priceless'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportReceiptPriceless(models.AbstractModel):
    #Reporte recepciones a deposito
    _name = 'report.wobin_reciba.report_receipt_priceless'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['receipt.priceless'].browse(docids)
        tickets_priceless = self.env['reciba.ticket'].search([('operation_type','=','in'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('destination_id','=',report.location.id),('state','=','priceless')])
        
        sum_net = 0
        count = 0
        for receipt in tickets_priceless:
            sum_net += receipt.net_weight
            count += 1
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net' : sum_net,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : tickets_priceless
        }

class ReceiptProducer(models.TransientModel):
    #Recepciones por productor    
    _name='receipt.producer'
    
    producer = fields.Many2one('res.partner', string="Productor")
    product = fields.Many2one('product.product', string="Producto")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportReceiptProducer(models.AbstractModel):
    #Reporte recepciones por productor
    _name = 'report.wobin_reciba.report_receipt_producer'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        report = self.env['receipt.producer'].browse(docids)
        tickets = self.env['reciba.ticket'].search([('operation_type','=','in'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('partner_id','=',report.producer.id),'|',('state','=','priceless'),('state','=','confirmed')])
        
        sum_net = 0
        count = 0
        tickets_producer = []
        for receipt in tickets:
            count += 1
            data = {
                'date':receipt.date.strftime("%d/%m/%Y"),
                'provider': receipt.partner_id.name,
                'name': receipt.name,
                'reception': '-',
                'net': "{:,.0f}".format(receipt.net_weight),
                'transfer': 'Sin movimiento',
                'status_invoiced': 'Sin facturar',
                'invoice': '-',
                'partner_invoice': '-',
                'invoice_status': '-'
            }
            if receipt.reception == 'price':
                data['reception'] = 'Con precio'
            elif receipt.reception == 'priceless':
                data['reception'] = 'Sin precio'
            if receipt.transfer_id:
                data['transfer'] = receipt.transfer_id.name
            if receipt.invoice_id:
                data['status_invoiced'] = 'Facturado'
                data['invoice'] = receipt.invoice_id.number
                data['partner_invoice'] = receipt.invoice_id.partner_id.name
                if receipt.invoice_id.state == 'draft':
                    data['invoice_status'] = 'Borrador'
                elif receipt.invoice_id.state == 'open':
                    data['invoice_status'] = 'Abierto'
                elif receipt.invoice_id.state == 'paid':
                    data['invoice_status'] = 'Pagado'
            tickets_producer.append(data)
        
        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'producer' : report.producer.name,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : tickets_producer
        }

class DeliveryUninvoiced(models.TransientModel):
    #Entregas por facturar    
    _name='delivery.uninvoiced'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportDeliveryUninvoiced(models.AbstractModel):
    #Reporte entregas por facturar
    _name = 'report.wobin_reciba.report_delivery_uninvoiced'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['delivery.uninvoiced'].browse(docids)
        tickets_uninvoiced = self.env['reciba.ticket'].search([('operation_type','=','out'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('origin_id','=',report.location.id),('state','=','confirmed'),('sale_invoice_status','=','to invoice')])
        
        sum_net = 0
        count = 0
        for delivery in tickets_uninvoiced:
            sum_net += delivery.net_weight
            count += 1
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net' : sum_net,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'deliveries' : tickets_uninvoiced
        }

class DeliveryInvoiced(models.TransientModel):
    #Entregas facturadas    
    _name='delivery.invoiced'
    
    product = fields.Many2one('product.product', string="Producto")
    location = fields.Many2one('stock.location', string="Ubicación")
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportDeliveryInvoiced(models.AbstractModel):
    #Reporte entregas facturadas
    _name = 'report.wobin_reciba.report_delivery_invoiced'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['delivery.invoiced'].browse(docids)
        tickets_invoiced = self.env['reciba.ticket'].search([('operation_type','=','out'),('date','>',report.init_date),('date','<',report.end_date),('product_id','=',report.product.id),('origin_id','=',report.location.id),('state','=','confirmed'),('sale_invoice_status','=','invoiced')])
        
        sum_net = 0
        count = 0
        for delivery in tickets_invoiced:
            sum_net += delivery.net_weight
            count += 1
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net' : sum_net,
            'count' : count
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'deliveries' : tickets_invoiced
        }

class QualityAvgHumidity(models.TransientModel):
    #Promedio ponderado de humedad    
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

        receipts = []
        for receipt in tickets_receipt:
            receipts.append({
                'name' : receipt.name,
                'date' : receipt.date.strftime("%d/%m/%Y %H:%M:%S"),
                'net_weight' : "{:,.0f}".format(receipt.net_weight),
                'humidity' : "{:.2f}".format(receipt.humidity)
            })
            sum_net_receipt += receipt.net_weight
            sum_humidity_receipt += receipt.net_weight * receipt.humidity
        avg_humidity_receipt = sum_humidity_receipt/sum_net_receipt

        deliveries = []
        for delivery in tickets_delivery:
            deliveries.append({
                'name' : delivery.name,
                'date' : delivery.date.strftime("%d/%m/%Y %H:%M:%S"),
                'net_weight' : "{:,.0f}".format(delivery.net_weight),
                'humidity' : "{:.2f}".format(delivery.humidity)
            })
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
            'today' : datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
            'product' : report.product.name,
            'location' : report.location.name,
            'sum_net_receipt' : "{:,.0f}".format(sum_net_receipt),
            'sum_humidity_receipt' : sum_humidity_receipt,
            'avg_humidity_receipt' : "{:.2f}".format(avg_humidity_receipt),
            'sum_net_delivery' : "{:,.0f}".format(sum_net_delivery),
            'sum_humidity_delivery' : sum_humidity_delivery,
            'avg_humidity_delivery' : "{:.2f}".format(avg_humidity_delivery),
            'dif_net' : "{:,.0f}".format(dif_net),
            'dif_avg' : "{:.2f}".format(dif_avg),
            'tolerance' : "{:,.0f}".format(tolerance),
            'decrease' : "{:,.0f}".format(decrease),
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'receipts' : receipts,
            'deliveries' : deliveries,
        }