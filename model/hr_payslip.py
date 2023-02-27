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
        boletas = self.env['boleta'].search([
            ('date', '>=', self.date_from), ('date', '<=', self.date_to),
            '|', '|', ('chofer', '=', self.employee_id.id), ('ayudante1', '=', self.employee_id.id), ('ayudante2', '=', self.employee_id.id)
        ])

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


class hr_payslip_report(models.Model):
    _name = "hr_payslip_report"

    def get_company(self):
        return self.env.company.id

    def obtener_planilla(self):
        self.env['hr_payslip_report_line'].search([('report', '=', self.id)]).unlink()
        planillas = self.env['hr.payslip'].search([('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])
        for planilla in planillas:
            salario = 0
            total = 0
            for line in planilla.line_ids:
                if line.code == "NET CHOFER":
                    salario = line.total
                #if line.code == "TOTAL":
                #    total = line.total
            depositado = salario - planilla.prestamo - planilla.ahorro
            self.env['hr_payslip_report_line'].create({
                'name': planilla.employee_id.id,
                'salario': salario,
                'prestamos': planilla.prestamo,
                'ahorro': planilla.ahorro,
                'bonif': planilla.bonific,
                'depositado': depositado,
                'date_del': planilla.date_from,
                'date_hasta': planilla.date_to,
                'report': self.id,
            })

        self.env['hr_payslip_report_gasto'].search([('report', '=', self.id)]).unlink()
        gastos = self.env['hr.payslip'].search([('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])
        for gasto in gastos:
            self.env['hr_payslip_report_gasto'].create({
                'name': gasto.employee_id.id,
                'peajes': 0,
                'noches': gasto.costo_noches,
                'por_viaje': 0,
                'adelanto': gasto.adelantos,
                'calzado': gasto.otras_deduc,
                'depositado': (0 + gasto.costo_noches + 0) - gasto.adelantos - gasto.otras_deduc,
                'fecha_del': gasto.date_from,
                'fecha_al': gasto.date_to,
                'report': self.id,
            })

    def planilla_to_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Planilla semanal',
            'view_mode': 'tree',
            'res_model': 'hr_payslip_report_line',
            'target': 'current',
        }

    def gastos_to_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Gastos semanal',
            'view_mode': 'tree',
            'res_model': 'hr_payslip_report_gasto',
            'target': 'current',
        }

    name = fields.Char("Name")
    company = fields.Many2one("res.company", string="Company", default=get_company)
    date_from = fields.Date("De")
    date_to = fields.Date("A")
    planillas = fields.One2many("hr_payslip_report_line", "report")
    gastos = fields.One2many("hr_payslip_report_gasto", "report")


class hr_payslip_report_line(models.Model):
    _name = "hr_payslip_report_line"
    _order = "name asc"

    name = fields.Many2one("hr.employee", string="Empleado")
    cedula = fields.Char(related="name.identification_id")
    oficio = fields.Many2one("hr.job", related="name.job_id")
    salario = fields.Float("Salario Semanal")
    prestamos = fields.Float("Prestamos")
    ahorro = fields.Float("Ahorro")
    bonif = fields.Float("Bonificaciones o feriados")
    depositado = fields.Float("Depositado")
    date_del = fields.Date("Del")
    date_hasta = fields.Date("Hasta")
    report = fields.Many2one("hr_payslip_report")


class hr_payslip_report_gasto(models.Model):
    _name = "hr_payslip_report_gasto"
    _order = "name asc"

    name = fields.Many2one("hr.employee", string="Empleado")
    oficio = fields.Many2one("hr.job", related="name.job_id")
    peajes = fields.Float("Peajes")
    noches = fields.Integer("Noches")
    por_viaje = fields.Float("Por viaje")
    adelanto = fields.Float("Adelanto")
    calzado = fields.Float("Calzado")
    depositado = fields.Float("Depositado")
    fecha_del = fields.Date("Del")
    fecha_al = fields.Date("Al")
    report = fields.Many2one("hr_payslip_report")