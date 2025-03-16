from odoo import models, fields


class ProjectProject(models.Model):
    _inherit = "project.project"

    is_gym_workout_plan = fields.Boolean(string="Is Gym Workout Plan?", default=False)
    workout_plan_description = fields.Text(string="Description")

    label_tasks = fields.Char(default="Workout Schedules")
