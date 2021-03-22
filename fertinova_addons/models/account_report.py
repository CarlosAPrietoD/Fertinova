

class ReceiptUninvoiced(models.TransientModel):
    #Recepciones por facturar    
    _name='account.lines'
    
    init_date = fields.Datetime(string="Fecha inicio")
    end_date = fields.Datetime(string="Fecha fin")

class ReportReceiptUninvoiced(models.AbstractModel):
    #Reporte recepciones por facturar
    _name = 'report.fertinova_addons.account_lines'

    @api.model
    def _get_report_values(self, docids, data=None):
        report = self.env['account.lines'].browse(docids)
        lines = self.env['account.move.line'].search([('date','>',report.init_date),('date','<',report.end_date)])
        

        report_data = {
            'i_date' : report.init_date.strftime("%d/%m/%Y"),
            'e_date': report.end_date.strftime("%d/%m/%Y"),
            'today' : date.today(),
        }

        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'report_data' : report_data,
            'lines' : lines
        }