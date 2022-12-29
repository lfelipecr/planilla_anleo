# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_employee_inherit_planilla(models.Model):
    _inherit = "hr.employee"

    codigo = fields.Integer("Código")