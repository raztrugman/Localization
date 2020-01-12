from odoo import fields, models, api
from odoo.exceptions import UserError


class ILSystem1000ImportFIles(models.TransientModel):
    _name = 'il.system.1000.import.files.wizard'
    _description = "System 1000 Import Files"

    sys1000_corrects_file = fields.Binary('Corrects File')
    sys1000_corrects_file_name = fields.Char()
    sys1000_incorrects_file = fields.Binary('Incorrects File')
    sys1000_incorrects_file_name = fields.Char()

    def process_system_1000_imports_files(self):
        def _process_incorrects_file():
            with open(self.sys1000_incorrects_file) as file:
                while True:
                    current_field = file.read(1)
                    if current_field != 'A':  # Field #38
                        raise UserError("Problem with parsing file (Header line)")
                        break
                    current_field = file.read(9)  # Field #39 Withholding tax ID
                    current_field = file.read(8)  # Field #40 Date
                    current_field = file.read(1)  # Field #41 / #47
                    if current_field != 'B' and current_field != 'Z':
                        raise UserError("Problem with parsing file (Vendors line)")
                        break
                    while current_field == 'B':
                        current_field = file.read(15)  # Field #42 Odoo ID
                        current_field = file.read(9)  # Field #43 Income Tax ID
                        current_field = file.read(9)  # Field #44 VAT ID Number
                        current_field = file.read(2)  # Field #45 Error code
                        current_field = file.read(50)  # Field #46 Error description
                        current_field = file.read(1)  # Field #40 / #47
                    if current_field != 'Z':
                        raise UserError("Problem with parsing file (Conclusion line)")
                        break
                    current_field = file.read(9)  # Field #48 Withholding tax ID (Same as field 39)
                    current_field = file.read(4)  # Field #49 number of vendors accepted in the export file
                    current_field = file.read(4)  # Field #50 number of corrects vendors
                    current_field = file.read(4)  # Field #51 number of incorrects vendors

                    file.close()
                    break

        def _process_corrects_file():
            with open(self.sys1000_corrects_file) as file:
                while True:
                    current_field = file.read(1)
                    if current_field != 'A':  # Field #10
                        raise UserError("Problem with parsing file (Header line)")
                        break
                    current_field = file.read(9)  # Field #11 Withholding tax ID
                    current_field = file.read(8)  # Field #12 Date
                    current_field = file.read(1)  # Field #13 / #33
                    if current_field != 'B' and current_field != 'Z':
                        raise UserError("Problem with parsing file (Vendors line)")
                        break
                    while current_field == 'B':
                        current_field = file.read(15)  # Field #14 Odoo ID
                        current_field = file.read(9)  # Field #15 Income Tax ID
                        current_field = file.read(9)  # Field #16 VAT ID Number
                        current_field = file.read(9)  # Field #17 Income Tax ID From SYSTEM 1000
                        current_field = file.read(9)  # Field #18 VAT ID Number From SYSTEM 1000
                        current_field = file.read(22)  # Field #19 Vendor name
                        current_field = file.read(1)  # Field #20 Confirmation of book management
                        current_field = file.read(2)  # Field #21
                        current_field = file.read(2)  # Field #22
                        current_field = file.read(2)  # Field #23
                        current_field = file.read(2)  # Field #24
                        current_field = file.read(2)  # Field #25
                        current_field = file.read(8)  # Field #26 Start date
                        current_field = file.read(8)  # Field #27 End date
                        current_field = file.read(8)  # Field #28 Confirmation date
                        current_field = file.read(3)  # Field #29
                        current_field = file.read(9)  # Field #30
                        current_field = file.read(10)  # Field #31 Max amount
                        current_field = file.read(9)  # Field #32
                        current_field = file.read(1)  # Field #13 / #33
                    if current_field != 'Z':
                        raise UserError("Problem with parsing file (Conclusion line)")
                        break
                    current_field = file.read(9)  # Field #48 Withholding tax ID (Same as field 39)
                    current_field = file.read(4)  # Field #49 number of vendors accepted in the export file
                    current_field = file.read(4)  # Field #50 number of corrects vendors
                    current_field = file.read(4)  # Field #51 number of incorrects vendors

                    file.close()
                    break

    def check_button(self):
        raise UserError("Test")





