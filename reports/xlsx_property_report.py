from docutils.nodes import header
from xlsxwriter import workbook, worksheet

from odoo import http
from ast import literal_eval
from odoo.http import request
import io
import xlsxwriter

class XlsxPropertyReport(http.Controller):
    @http.route('/property/excel/report/<string:property_ids>', type='http',auth='user')
    def download_property_xlsx_report(self,property_ids):
        property_ids=request.env['property'].browse(literal_eval(property_ids))
        print(property_ids)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in memory':True})
        worksheet = workbook.add_worksheet('properties')
        header_formate = workbook.add_format({'bold':True})
        string_formate = workbook.add_format({'bold':True,'align':'center'})
        price_formate = workbook.add_format({'num_format':'$##,##00.00','bold':True,'align':'center'})
        headers= ['name','postcode','Garden']
        for col_num,header in enumerate(headers) :

            worksheet.write(0,col_num,header,header_formate)
        row_num=1
        for property in property_ids:
            worksheet.write(row_num,0,property.name,string_formate)
            worksheet.write(row_num,1,property.postcode,price_formate)
            worksheet.write(row_num,2,'yes'if property.garden else 'no',string_formate)
            row_num +=1
        workbook.close()
        output.seek(0)
        file_name = 'Property Report.xlsx'
        return request.make_response(
            output.getvalue(),headers =[('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                                        ('Content-Disposition',f'attachment;filename={file_name}')]
        )