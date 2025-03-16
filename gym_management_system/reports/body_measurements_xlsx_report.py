from odoo import models


class BodyMeasurementsXlsx(models.AbstractModel):
    _name = 'report.gym_management_system.body_measurements_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = "Abstract XLSX Report For Body Measurements"


    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Body Measurements Report')

        # Formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#4F81BD',
            'font_color': 'white'
        })
        subtitle_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'left',
            'valign': 'vcenter',
            'font_color': 'black'
        })
        header_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9EAD3',
            'border': 1
        })
        bold = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        date_format = workbook.add_format({
            'num_format': 'dd-yyyy-mm',
            'align': 'center',
            'border': 1
        })
        normal_format = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })

        # Column widths
        sheet.set_column(0, 0, 25)  # Date
        sheet.set_column(1, 1, 20)  # Weight
        sheet.set_column(2, 2, 20)  # BMI
        sheet.set_column(3, 3, 20)  # Chest
        sheet.set_column(4, 4, 20)  # Right Arm
        sheet.set_column(5, 5, 20)  # Left Arm
        sheet.set_column(6, 6, 20)  # Hip
        sheet.set_column(7, 7, 20)  # Right Thigh
        sheet.set_column(8, 8, 20)  # Left Thigh
        sheet.set_column(9, 9, 20)  # Right Calf
        sheet.set_column(10, 10, 20)  # Left Calf

        sheet.merge_range('A1:K1', 'BODY MEASUREMENTS REPORT', title_format)

        if lines:
            sheet.merge_range('A3:C3', f"Member Name: {lines[0].member_id.name}", subtitle_format)

        header = ['Date', 'Weight', 'BMI', 'Chest', 'Right Arm', 'Left Arm', 'Hip', 'Right Thigh', 'Left Thigh', 'Right Calf', 'Left Calf']
        for col, field_name in enumerate(header):
            sheet.write(4, col, field_name, header_format)

        # Data rows
        row = 5
        for line in lines:
            sheet.write(row, 0, line.date, date_format)
            sheet.write(row, 1, line.weight, normal_format)
            sheet.write(row, 2, line.bmi, normal_format)
            sheet.write(row, 3, line.chest, normal_format)
            sheet.write(row, 4, line.right_arm, normal_format)
            sheet.write(row, 5, line.left_arm, normal_format)
            sheet.write(row, 6, line.hip, normal_format)
            sheet.write(row, 7, line.right_thigh, normal_format)
            sheet.write(row, 8, line.left_thigh, normal_format)
            sheet.write(row, 9, line.right_calf, normal_format)
            sheet.write(row, 10, line.left_calf, normal_format)
            row += 1
