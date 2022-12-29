# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class planilla_viaticos(models.Model):
    _name = "viaticos"
    _description = "viaticos"

    name = fields.Char("Nombre", default="Viáticos")
    feriados = fields.Float("Feriados")
    noches = fields.Float("Noches")
    locos = fields.Float("Locos")