# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class hr_payslip_inherit_planilla(models.Model):
    _inherit = "hr.payslip"

    @api.onchange("cant_locos")
    def change_locos(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_locos = viaticos.locos * self.cant_locos

    @api.onchange("cant_noches")
    def change_noches(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_noches = viaticos.noches * self.cant_noches

    @api.onchange("cant_feriados")
    def change_feriados(self):
        viaticos = self.env['viaticos'].search([], limit=1)
        self.costo_feriados = viaticos.feriados * self.cant_feriados

    def get_neto(self):
        for rec in self:
            rec.total_neto = 0
            for line in rec.line_ids:
                if line.code == "NET":
                    rec.total_neto = line.total

    def get_viaticos(self):
        for rec in self:
            rec.total_viaticos = 0
            for line in rec.line_ids:
                if line.code == "VIAT":
                    rec.total_viaticos = line.total

    def get_total(self):
        for rec in self:
            rec.total_pagar = 0
            for line in rec.line_ids:
                if line.code == "TOTAL":
                    rec.total_pagar = line.total

    def get_boletas(self):
        viajes = 0
        costo_viajes = 0
        boletas = self.env['boleta'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to), ('chofer', '=', self.employee_id.id)])

        viajes = len(boletas)
        for boleta in boletas:
            costo_viajes = costo_viajes + boleta.costo_viaticos

        self.cant_viajes = viajes
        self.costo_viajes = costo_viajes

    codigo = fields.Integer(related="employee_id.codigo", string="Código Empleado")
    semana_pagar = fields.Integer("Semana a Pagar")
    saldo_prestamo = fields.Float("Saldo Préstamo")
    fecha_pago = fields.Date("Fecha Pago")

    #viajes
    cant_viajes = fields.Integer("Cant. Viajes")
    costo_viajes = fields.Float("Costo Viajes")

    cant_locos = fields.Integer("Cant. Locos")
    costo_locos = fields.Float("Costo Locos")
    cant_noches = fields.Integer("Cant. Noches")
    costo_noches = fields.Float("Costo Noches")
    cant_feriados = fields.Integer("Cant. Feriados")
    costo_feriados = fields.Float("Costo Feriados")

    otros_viajes = fields.Float("Otros Viajes")

    carga = fields.Float("Carga/Descarga")
    bonific = fields.Float("Bonific.")
    reintegros = fields.Float("Reintegros")

    #deducciones
    deduc_obrera = fields.Float("Deduc. Obrera")
    prestamo = fields.Float("Préstamo")
    ahorro = fields.Float("Ahorro")
    otras_deduc = fields.Float("Otras Deduc.")
    adelantos = fields.Float("Adelantos")

    total_neto = fields.Float("Neto", compute="get_neto")
    total_viaticos = fields.Float("Viáticos", compute="get_viaticos")
    total_pagar = fields.Float("Total", compute="get_total")