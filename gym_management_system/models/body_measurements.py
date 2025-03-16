from odoo import models, fields, api
from datetime import date


class BodyMeasurements(models.Model):
    _name = "body.measurements"
    _description = "Body Measurements"
    _rec_name = "member_id"

    user_id = fields.Many2one("res.users",default=lambda self: self.env.user, string="User")
    member_id = fields.Many2one("res.partner", string="Member", compute="_compute_member_id", store=True)
    date = fields.Date(string="Date", default=date.today())
    height = fields.Float(string="Height(in cm)", compute="_compute_height", store=True)
    weight = fields.Float(string="Weight(in kg)", required=True)
    bmi = fields.Float(string="BMI", compute="_compute_bmi", store=True)
    chest = fields.Float(string="Chest")
    right_arm = fields.Float(string="Right Arm")
    left_arm = fields.Float(string="Left Arm")
    hip = fields.Float(string="Hip")
    right_thigh = fields.Float(string="Right Thigh")
    left_thigh = fields.Float(string="Left Thigh")
    right_calf = fields.Float(string="Right Calf")
    left_calf = fields.Float(string="Left Calf")

    @api.depends("height", "weight")
    def _compute_bmi(self):
        for record in self:
            if record.height > 0 and record.weight > 0:
                height_in_m = record.height / 100
                bmi = record.weight / (height_in_m**2)
                record.bmi = round(bmi, 2)


    @api.depends('user_id')
    def _compute_member_id(self):
        for rec in self:
            rec.member_id = rec.user_id.partner_id

    
    @api.depends('member_id')
    def _compute_height(self):
        for rec in self:
            rec.height = rec.member_id.height