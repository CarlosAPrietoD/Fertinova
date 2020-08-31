from odoo import models, fields, api
import xlrd
import tempfile
import binascii
from datetime import datetime

class FuelWizard(models.TransientModel):
    _name = "import.templates.wizard"

    #----------------------------------------------------------------------------
    #--SC_FN.TA_TK-Interno 00100 Importar Plantilla de combustible en compras.---
    #--SC_FN.TA_TK-Interno 00101 Importar Plantilla de casetas en contabilidad---
    #----------------------------------------------------------------------------
    file_xls=fields.Binary(string='Excel File')

    '''def current_date_format(self, date):
        months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
        day = date.day
        month = months[date.month - 1]
        year = date.year
        messsage = "Casetas {} {}".format(month, year)

        return messsage'''

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
        
            data=[]
            total_debit = 0
            total_credit = 0
            final_debit = 0
            final_credit = 0
            

            for row_no in range(sheet_fuel.nrows):
                #recorremos los renglones del excel y vamos guardando los datos en un objeto nuevo
                if row_no <= 0:
                    fields = map(lambda row:row.value, sheet_fuel.row(row_no))
                else:
                    lines = list(map(lambda row:isinstance(row.value, str) and row.value or str(row.value), sheet_fuel.row(row_no)))
                    if lines[0] != b'Cuenta':
                        
                        account = False
                        partner = False
                        label = ''
                        a_account = False
                        a_label = False
                        debit = 0
                        credit = 0
                        taxes = False

                        #hacemos las busquedas de ids de otros modelos que necesitemos
                        
                        if lines[0] != '':
                            account = self.env['account.account'].search([('code','=',lines[0])], limit=1).id
                        if lines[1] != '':
                            partner = self.env['res.partner'].search([('name','ilike',lines[1])], limit=1).id
                        if lines[2] != '':
                            label = lines[2]
                        if lines[3] != '':
                            a_account = self.env['account.analytic.account'].search([('name','=',lines[3])], limit=1).id
                        if lines[4] != '':
                            a_label_id = self.env['account.analytic.tag'].search([('name','=',lines[4])], limit=1).id
                            if a_label_id:
                                a_label = [(4,a_label_id)]
                        if lines[5] != '':
                            debit = lines[5]
                        if lines[6] != '':
                            credit = lines[6]
                        if lines[7] != '':
                            tax_id = self.env['account.tax'].search([('name','=',lines[7])], limit=1).id
                            if tax_id:
                                taxes = [(4,tax_id)]

                        #objeto con todos los datos de la linea del excel

                        data_object = { 'account_id' : account,
                                        'partner_id' : partner,
                                        'name' : label,
                                        'analytic_account_id' : a_account,
                                        'analytic_tag_ids' : a_label,
                                        'debit' : float(debit),
                                        'credit' : float(credit),
                                        'tax_ids' : taxes
                                    }

                        data.append((0,0,data_object))

                        #sumamos todos los credito y debito para hacer la comparacion
                        
                        total_credit += float(credit)
                        total_debit += float(debit)

            #guardamos la diferencia en una variable para hacer cuadrar el credito y debito

            if total_credit > total_debit:
                final_debit = total_credit - total_debit
            else:
                final_credit = total_debit - total_credit

            #agregamos un ultimo renglon con la diferencia

            account_dif = self.env['account.account'].search([('code','=','201.01.001')], limit=1).id
        
            difference = { 'account_id' : account_dif,
                            'debit' : final_debit,
                            'credit' : final_credit
                        }
            
            data.append((0,0,difference))

            #creamos el nuevo registro con todas las lineas

            journal = self.env['account.journal'].search([('name','=','TA. Provisiones')], limit=1).id

            vals = {
                    'ref': 'Diesel Nuevo',
                    'journal_id': journal,
                    'line_ids' : data
                }

            record = self.env['account.move'].create(vals)

        #=============================Tollbooth invoice==========================

        try:
            sheet_toll = workbook.sheet_by_name("Odoo Factura Casetas")
        except:
            sheet_toll = ""

        if sheet_toll != "":
            #load the data in an array "data"

            data=[]
            total_debit = 0
            total_credit = 0
            final_debit = 0
            final_credit = 0
            

            for row_no in range(sheet_toll.nrows):
                #recorremos los renglones del excel y vamos guardando los datos en un objeto nuevo
                if row_no <= 0:
                    fields = map(lambda row:row.value, sheet_toll.row(row_no))
                else:
                    lines = list(map(lambda row:isinstance(row.value, str) and row.value or str(row.value), sheet_toll.row(row_no)))
                    if lines[0] != b'Cuenta':
                        
                        account = False
                        partner = False
                        label = ''
                        a_account = False
                        a_label = False
                        debit = 0
                        credit = 0
                        taxes = False

                        #hacemos las busquedas de ids de otros modelos que necesitemos
                        
                        if lines[0] != '':
                            account = self.env['account.account'].search([('code','=',lines[0])], limit=1).id
                        if lines[1] != '':
                            partner = self.env['res.partner'].search([('name','ilike',lines[1])], limit=1).id
                        if lines[2] != '':
                            label = lines[2]
                        if lines[3] != '':
                            a_account = self.env['account.analytic.account'].search([('name','=',lines[3])], limit=1).id
                        if lines[4] != '':
                            a_label_id = self.env['account.analytic.tag'].search([('name','=',lines[4])], limit=1).id
                            if a_label_id:
                                a_label = [(4,a_label_id)]
                        if lines[5] != '':
                            debit = lines[5]
                        if lines[6] != '':
                            credit = lines[6]
                        if lines[7] != '':
                            tax_id = self.env['account.tax'].search([('name','=',lines[7])], limit=1).id
                            if tax_id:
                                taxes = [(4,tax_id)]

                        #objeto con todos los datos de la linea del excel

                        data_object = { 'account_id' : account,
                                        'partner_id' : partner,
                                        'name' : label,
                                        'analytic_account_id' : a_account,
                                        'analytic_tag_ids' : a_label,
                                        'debit' : float(debit),
                                        'credit' : float(credit),
                                        'tax_ids' : taxes
                                    }

                        data.append((0,0,data_object))

                        #sumamos todos los credito y debito para hacer la comparacion
                        
                        total_credit += float(credit)
                        total_debit += float(debit)

            #guardamos la diferencia en una variable para hacer cuadrar el credito y debito

            if total_credit > total_debit:
                final_debit = total_credit - total_debit
            else:
                final_credit = total_debit - total_credit

            #agregamos un ultimo renglon con la diferencia

            account_dif = self.env['account.account'].search([('code','=','201.01.001')], limit=1).id
        
            difference = { 'account_id' : account_dif,
                            'debit' : final_debit,
                            'credit' : final_credit
                        }
            
            data.append((0,0,difference))

            #creamos el nuevo registro con todas las lineas

            journal = self.env['account.journal'].search([('name','=','TA. Provisiones')], limit=1).id

            vals = {
                    'ref': 'Casetas Nuevo',
                    'journal_id': journal,
                    'line_ids' : data
                }

            record = self.env['account.move'].create(vals)
            

        #=============================Contributions invoice==========================

        try:
            sheet_toll = workbook.sheet_by_name("Aportaciones")
        except:
            sheet_toll = ""

        if sheet_toll != "":
            #load the data in an array "data"

            data=[]
            total_debit = 0
            total_credit = 0
            final_debit = 0
            final_credit = 0
            

            for row_no in range(sheet_toll.nrows):
                #recorremos los renglones del excel y vamos guardando los datos en un objeto nuevo
                if row_no <= 0:
                    fields = map(lambda row:row.value, sheet_toll.row(row_no))
                else:
                    lines = list(map(lambda row:isinstance(row.value, str) and row.value or str(row.value), sheet_toll.row(row_no)))
                    if lines[0] != b'Cuenta':
                        
                        account = False
                        partner = False
                        label = ''
                        a_account = False
                        a_label = False
                        debit = 0
                        credit = 0

                        #hacemos las busquedas de ids de otros modelos que necesitemos
                        
                        if lines[0] != '':
                            account = self.env['account.account'].search([('code','=',lines[0])], limit=1).id
                        if lines[2] != '':
                            partner = self.env['res.partner'].search([('name','ilike',lines[2])]).id
                        if lines[3] != '':
                            label = lines[3]
                        if lines[4] != '':
                            a_account = self.env['account.analytic.account'].search([('name','=',lines[4])], limit=1).id
                        if lines[5] != '':
                            a_label_id = self.env['account.analytic.tag'].search([('name','=',lines[5])], limit=1).id
                            if a_label_id:
                                a_label = [(4,a_label_id)]
                        if lines[6] != '':
                            debit = lines[6]
                        if lines[7] != '':
                            credit = lines[7]
                        

                        #objeto con todos los datos de la linea del excel

                        data_object = { 'account_id' : account,
                                        'partner_id' : partner,
                                        'name' : label,
                                        'analytic_account_id' : a_account,
                                        'analytic_tag_ids' : a_label,
                                        'debit' : float(debit),
                                        'credit' : float(credit)
                                    }

                        data.append((0,0,data_object))

                        #sumamos todos los credito y debito para hacer la comparacion
                        
                        total_credit += float(credit)
                        total_debit += float(debit)

            #guardamos la diferencia en una variable para hacer cuadrar el credito y debito

            if total_credit > total_debit:
                final_debit = total_credit - total_debit
            else:
                final_credit = total_debit - total_credit

            #agregamos un ultimo renglon con la diferencia

            account_dif = self.env['account.account'].search([('code','=','201.01.001')], limit=1).id
        
            difference = { 'account_id' : account_dif,
                            'debit' : final_debit,
                            'credit' : final_credit
                        }
            
            data.append((0,0,difference))

            #creamos el nuevo registro con todas las lineas

            journal = self.env['account.journal'].search([('name','=','TA. Provisiones')], limit=1).id

            vals = {
                    'ref': 'Aportaciones Nuevo',
                    'journal_id': journal,
                    'line_ids' : data
                }

            record = self.env['account.move'].create(vals)
            


    #----------------------------------------------------------------------------
    #---------------SC_FN.TA_TK-Interno 00100 Fin del desarrollo-----------------
    #----------------------------------------------------------------------------

            
                