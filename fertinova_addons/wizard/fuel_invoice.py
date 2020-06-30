from odoo import models, fields, api
import xlrd
import tempfile
import binascii
from datetime import date

class FuelWizard(models.TransientModel):
    _name = "fuel.wizard"

    #----------------------------------------------------------------------------
    #--SC_FN.TA_TK-Interno 00100 Importar Plantilla de combustible en compras.---
    #----------------------------------------------------------------------------
    file_xls=fields.Binary(string='Excel File')

    @api.multi
    def import_fuel_xls(self):
        
        #read the xls file in the sheet 'Reporte de Asistencias'
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file_xls))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)

        #==================================Fuel invoice==========================================

        try:
            sheet_fuel = workbook.sheet_by_name("Odoo Factura Diesel")
        except:
            sheet_fuel = ""

        if sheet_fuel != "":
        
            #load the data in an array "data"
            provider=""
            product1=""
            product2=""
            p_n=-1
            data=[]
            for row_no in range(sheet_fuel.nrows):
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet_fuel.row(row_no))
                else:
                    lines = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet_fuel.row(row_no)))
                    
                    if lines[1]==b'Proveedor':
                        provider=lines[2].decode("utf-8")
                        p_n=row_no+1

                    if p_n == row_no:
                        if lines[0] != "":
                            product1 = lines[0].decode("utf-8")
                        if lines[7] != "":
                            product2 = lines[7].decode("utf-8")
                    
                    if lines[0]!='':
                        if lines[0].decode("utf-8").find('DIESEL') >= 0:
                            data.append(lines)
            
            #Search related fields

            partner=0
            if provider!="":
                partner = self.env['res.partner'].search([('name','=',provider)]).id

            product1_id=0
            if product1!="":
                product1_id = self.env['product.product'].search([('default_code','=',product1)]).id

            product2_id=0
            if product2!="":
                product2_id = self.env['product.product'].search([('default_code','=',product2)]).id
            
            account = self.env['account.account'].search([('code','=','501.01.002')]).id

            account_ieps = self.env['account.account'].search([('code','=','501.01.010')]).id


            #Create invoice
            vals = {
                    'type': 'in_invoice',
                    'partner_id' : partner,
                }
            record = self.env['account.invoice'].create(vals)

            for d in data:

                uom = self.env['uom.uom'].search([('name','=',d[5].decode("utf-8"))]).id

                iva_16 = self.env['account.tax'].search([('name','=',d[6].decode("utf-8"))]).id

                if iva_16 == False:
                    iva_16=0

                iva_ex = self.env['account.tax'].search([('name','=',d[13].decode("utf-8"))]).id

                if iva_ex == False:
                    iva_ex=0

                #Create invoice lines
                a_account = self.env['account.analytic.account'].search([('name','=',d[1].decode("utf-8"))]).id
                
                a_tag = self.env['account.analytic.tag'].search([('name','=',d[2].decode("utf-8"))]).id
                
                if a_tag == False:
                    a_tag=0
                
                line_vals = {
                        'product_id': product1_id,
                        'name': d[0].decode("utf-8"),
                        'quantity': d[3],
                        'price_unit' : d[4],
                        'uom_id': uom,
                        'account_id': account,
                        'account_analytic_id': a_account
                    }

                line = self.env['account.invoice.line'].create(line_vals)

                if iva_16 != 0:
                    line.invoice_line_tax_ids=[(4,iva_16)]
                
                if a_tag != 0:
                    line.analytic_tag_ids=[(4,a_tag)]
                
                record.invoice_line_ids=[(4,line.id)]

                line_vals = {
                        'product_id': product2_id,
                        'name': d[7].decode("utf-8"),
                        'quantity': d[10],
                        'price_unit' : d[12],
                        'uom_id': uom,
                        'account_id': account_ieps,
                        'account_analytic_id': a_account,
                    }

                line = self.env['account.invoice.line'].create(line_vals)

                if iva_ex != 0:
                    line.invoice_line_tax_ids=[(4,iva_ex)]
                
                if a_tag != 0:
                    line.analytic_tag_ids=[(4,a_tag)]

                record.invoice_line_ids=[(4,line.id)]

            taxes_grouped = record.get_taxes_values()
            tax_lines = record.tax_line_ids.filtered('manual')
            for tax in taxes_grouped.values():
                tax_lines += tax_lines.new(tax)
            record.tax_line_ids = tax_lines

        #=============================Tollbooth invoice==========================

        try:
            sheet_toll = workbook.sheet_by_name("Odoo Factura Casetas")
        except:
            sheet_toll = ""

        if sheet_toll != "":
            #load the data in an array "data"
            provider=""
            product=""
            p_n=-1
            data=[]
            for row_no in range(sheet_toll.nrows):
                
                if row_no <= 0:
                    fields = map(lambda row:row.value.encode('utf-8'), sheet_toll.row(row_no))
                else:
                    lines = list(map(lambda row:isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value), sheet_toll.row(row_no)))
                    
                    if lines[1]==b'Proveedor':
                        provider=lines[2].decode("utf-8")
                        p_n=row_no+1

                    if p_n == row_no:
                        if lines[0] != "":
                            product = lines[0].decode("utf-8")
                    
                    if lines[0]!='':
                        if lines[0].decode("utf-8").find('Casetas') >= 0:
                            data.append(lines)

            
            #Search related fields

            partner=0
            if provider!="":
                partner = self.env['res.partner'].search([('name','=',provider)]).id

            product_id=0
            if product!="":
                product_id = self.env['product.product'].search([('default_code','=',product)]).id
            
            account = self.env['account.account'].search([('code','=','501.01.004')]).id

            #Create invoice
            vals = {
                    'type': 'in_invoice',
                    'partner_id' : partner,
                }
            record = self.env['account.invoice'].create(vals)

            for d in data:

                uom = self.env['uom.uom'].search([('name','=',d[5].decode("utf-8"))]).id

                iva_16 = self.env['account.tax'].search([('name','=',d[6].decode("utf-8"))]).id

                if iva_16 == False:
                    iva_16=0

                #Create invoice lines
                a_account = self.env['account.analytic.account'].search([('name','=',d[1].decode("utf-8"))]).id
                
                a_tag = self.env['account.analytic.tag'].search([('name','=',d[2].decode("utf-8"))]).id
                
                if a_tag == False:
                    a_tag=0
                
                line_vals = {
                        'product_id': product_id,
                        'name': d[0].decode("utf-8"),
                        'quantity': d[3],
                        'price_unit' : d[4],
                        'uom_id': uom,
                        'account_id': account,
                        'account_analytic_id': a_account
                    }

                line = self.env['account.invoice.line'].create(line_vals)

                if iva_16 != 0:
                    line.invoice_line_tax_ids=[(4,iva_16)]
                
                if a_tag != 0:
                    line.analytic_tag_ids=[(4,a_tag)]
                
                record.invoice_line_ids=[(4,line.id)]

            taxes_grouped = record.get_taxes_values()
            tax_lines = record.tax_line_ids.filtered('manual')
            for tax in taxes_grouped.values():
                tax_lines += tax_lines.new(tax)
            record.tax_line_ids = tax_lines

    #----------------------------------------------------------------------------
    #---------------SC_FN.TA_TK-Interno 00100 Fin del desarrollo-----------------
    #----------------------------------------------------------------------------

            
                