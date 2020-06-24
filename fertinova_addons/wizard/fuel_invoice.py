from odoo import models, fields, api
import xlrd
import tempfile
import binascii

class FuelWizard(models.TransientModel):
    _name = "fuel.wizard"

    file_xls=fields.Binary(string='Excel File')

    @api.multi
    def import_fuel_xls(self):
        
        #read the xls file in the sheet 'Reporte de Asistencias'
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file_xls))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_name("Odoo Factura Diesel")
        
        #load the data in an array "data"
        provider=""
        data=[]
        for row_no in range(sheet.nrows):
            if row_no <= 0:
                fields = map(lambda row:row.value.encode('utf-8'), sheet.row(row_no))
            else:
                lines = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet.row(row_no)))
                
                if lines[1]==b'Proveedor':
                    provider=lines[2].decode("utf-8")
                
                if lines[0]!='':
                    if lines[0].decode("utf-8").find('DIESEL') >= 0:
                        data.append(lines)
        

        partner=""
        if provider!="":
            partner = self.env['res.partner'].search([('name','=',provider)])
        
        account = self.env['account.account'].search([('name','=','COMBUSTIBLE')]).id

        account_ieps = self.env['account.account'].search([('name','=','IEPS COMBUSTIBLE')]).id

        uom = self.env['uom.uom'].search([('name','=','Servicio(s)')]).id

        iva_16 = self.env['account.tax'].search([('name','=','IVA(16%) COMPRAS')]).id

        iva_ex = self.env['account.tax'].search([('name','=','IVA(Exento) COMPRAS')]).id

        product = self.env['product.product'].search([('default_code','=','SERV007')]).id


        vals = {
                'type': 'in_invoice',
                'partner_id' : partner.id
            }
        record = self.env['account.invoice'].create(vals)


        for d in data:
            line_vals = {
                    'name': d[0].decode("utf-8"),
                    'quantity': d[3],
                    'price_unit' : d[4],
                    'uom_id': uom,
                    'account_id': account,
                    'invoice_line_tax_ids': [(4,iva_16)]
                }

            line = self.env['account.invoice.line'].create(line_vals)
            
            record.invoice_line_ids=[(4,line.id)]

            line_vals = {
                    'product_id': product,
                    'name': d[7].decode("utf-8"),
                    'quantity': d[10],
                    'price_unit' : d[12],
                    'uom_id': uom,
                    'account_id': account_ieps,
                    'invoice_line_tax_ids': [(4,iva_ex)]
                }
            
            line = self.env['account.invoice.line'].create(line_vals)

            record.invoice_line_ids=[(4,line.id)]


        

        #record.invoice_line_ids=[(4, record_line.id)]

        '''for d in data:
            self.env[]'''
            
                