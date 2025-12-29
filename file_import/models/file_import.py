import base64
import csv
import json
import io

from odoo import models, fields
from odoo.exceptions import UserError


class FileImport(models.TransientModel):
    _name = 'file.import'
    _description = 'File Import Wizard'

    file_data = fields.Binary('File', required=True)
    file_name = fields.Char('File Name')

    file_type = fields.Selection([
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('txt', 'Text'),
        ('xml', 'XML'),
        ('xlsx', 'Excel (XLSX)'),
        ('pdf', 'PDF'),
    ], string='File Type', required=True)

    # =====================
    # Main Button Method
    # =====================
    def process_file(self):
        self.ensure_one()

        if not self.file_data:
            raise UserError('Please select a file')

        content = base64.b64decode(self.file_data)

        # Map file types to processing methods
        processors = {
            'xlsx': self._process_xlsx,
            'csv': self._process_csv,
            'json': self._process_json,
            'txt': self._process_txt,
            'xml': self._process_xml,
            'pdf': self._process_pdf,  # optional: if you plan to parse PDFs
        }

        process_func = processors.get(self.file_type)
        if not process_func:
            raise UserError(f"File type {self.file_type} is not supported")

        data = process_func(content)

        # Example: for products only, you may still call import
        if self.file_type in ('xlsx', 'csv', 'json'):
            self._import_products(data)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import Successful',
                'message': f'{len(data)} records processed successfully.',
                'type': 'success',
                'sticky': False,
            }
        }

    # =====================
    # Excel Reader
    # =====================
    def _process_xlsx(self, content):
        import openpyxl
        from zipfile import BadZipFile

        try:
            wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
        except BadZipFile:
            raise UserError(
                "Invalid Excel file.\n"
                "Please upload a valid .xlsx file."
            )

        sheet = wb.active

        headers = [str(c.value).strip() for c in sheet[1]]
        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = dict(zip(headers, row))
            data.append(row_data)

        return data

    # =====================
    # Product Import Logic
    # =====================
    def _import_products(self, data):
        Product = self.env['product.template'].sudo()

        for row in data:
            if not row.get('name'):
                continue

            vals = {
                'name': row.get('name'),
                'default_code': row.get('default_code'),
                'list_price': float(row.get('list_price') or 0),
                'standard_price': float(row.get('standard_price') or 0),
                'type': row.get('type') or 'product',
                'active': True,
                'company_id': self.env.company.id,
            }

            product = False
            if vals.get('default_code'):
                product = Product.search(
                    [('default_code', '=', vals['default_code'])],
                    limit=1
                )

            if product:
                product.write(vals)
            else:
                Product.create(vals)
