from odoo import fields, models, api
from datetime import date
import zipfile
import io
import base64
from contextlib import closing
from odoo.exceptions import UserError


class ILSystem1000ImportFIles(models.TransientModel):
    _name = 'il.system.1000.import.files.wizard'
    _description = "System 100 Import Files"

    my_company_id = fields.Many2one('res.company', string='Company to export',
                                    required=True, default=lambda self: self.env.user.company_id)
    unified_system_1000_data = fields.Binary('Unified System 1000 Data', readonly=True)
    filename = fields.Text(default='system_1000_export_files.zip', readonly=True)

    def _compute_my_companies_field(self):
        related_record_set = self.env['res.users'].search([('company_ids', '=', self.my_company_id.id)])
        self.my_companies = related_record_set

    def prepare_one_file_of_system_1000_data(self, suppliers):
        file_data = ""
        number_of_suppliers = 0

        def _prepare_header_line():
            data = ""
            data += "A"  # Field number 1
            if self.my_company_id.l10n_il_withh_tax_id_number:
                if len(self.my_company_id.l10n_il_withh_tax_id_number) != 9 or \
                        str(self.my_company_id.l10n_il_withh_tax_id_number)[0] != '9':
                    raise UserError("Please assign appropriate withholding tax ID number!")
                else:
                    data += str(self.my_company_id.l10n_il_withh_tax_id_number)  # Field number 2
            else:
                raise UserError("Please assign your withholding tax ID number!")
            return data

        def _prepare_inner_data(one_supplier):
            data = ""
            data += "B"  # Field number 3
            data += str(one_supplier.id).zfill(15)  # Field number 4
            if one_supplier.l10n_il_income_tax_id_number:
                data += str(one_supplier.l10n_il_income_tax_id_number).zfill(9)  # Field number 5
            else:
                data += "".zfill(9)
            if one_supplier.vat:
                data += str(one_supplier.vat).zfill(9)  # Field number 6
            else:
                data += "".zfill(9)
            return data

        def _prepare_closing_line():
            data = ""
            data += "Z"  # Field number 7
            data += str(self.my_company_id.l10n_il_withh_tax_id_number).zfill(9)  # Field number 8
            data += str(number_of_suppliers).zfill(4)  # Field number 9
            return data

        # Create export data up to 1000 suppliers
        file_data += _prepare_header_line()

        for supplier in suppliers:
            file_data += _prepare_inner_data(supplier)
            number_of_suppliers += 1

        file_data += _prepare_closing_line()

        return file_data

    def export_system_1000_files(self):
        today_date = date.today().strftime("%d%m%Y")
        file_format = '.txt'

        suppliers = self.env['res.partner'].search([('supplier_rank', '>', 0)])
        number_of_suppliers = len(suppliers)

        with closing(io.BytesIO()) as f:
            with zipfile.ZipFile(f, 'w') as archive:
                #  Up to 1000 suppliers
                if number_of_suppliers <= 1000:
                    file_number = 1
                    file_name = str(self.my_company_id.l10n_il_withh_tax_id_number) + '_' + today_date + '_' + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                #  Between 1000 to 2000 suppliers
                elif number_of_suppliers <= 2000:
                    file_number = 1
                    file_name = str(self.my_company_id.l10n_il_withh_tax_id_number) + "_" + today_date + "_" + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                    file_number = 2
                    file_name = self.my_company_id.l10n_il_withh_tax_id_number + "_" + today_date + "_" + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[1000:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                #  Between 2000 to 3000 suppliers
                elif number_of_suppliers <= 3000:
                    file_number = 1
                    file_name = self.my_company_id.l10n_il_withh_tax_id_number + "_" + today_date + "_" + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                    file_number = 2
                    file_name = self.my_company_id.l10n_il_withh_tax_id_number + "_" + today_date + "_" + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[1000:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                    file_number = 3
                    file_name = self.my_company_id.l10n_il_withh_tax_id_number + "_" + today_date + "_" + str(file_number).zfill(3) + file_format
                    system_1000_data = self.prepare_one_file_of_system_1000_data(suppliers[2000:number_of_suppliers])
                    archive.writestr(file_name, system_1000_data.encode('utf-8'))

                #  Over 3000 suppliers - Exception
                else:
                    raise UserError("System 1000 don't support over 3000 suppliers")

            zip_data = f.getvalue()
        self.write({'unified_system_1000_data': base64.encodestring(zip_data)})

        action = {
            'type': 'ir.actions.act_url',
            'url': "web/content/?model=il.system.1000.export.file.wizard&id=" + str(self.id) +
                   "&filename_field=filename&field=unified_system_1000_data&download=true&filename=" + self.filename,
            'target': 'self'
        }
        return action


