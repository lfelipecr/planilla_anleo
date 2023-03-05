# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class boleta(models.Model):
    _name = "boleta"
    _inherit = ['mail.thread']
    _description = "Boleta"

    @api.onchange("ruta")
    def change_ruta(self):
        self.costo_viaje = self.ruta.costo_viaje
        self.costo_viaticos = self.ruta.costo_viaticos

    @api.model
    def create(self, vals):
        rec = super(boleta, self).create(vals)
        rec.name = rec.id

        #product_id = self.env['product.product'].search([('product_tmpl_id', '=', rec.producto.id)], limit=1)

        registro = self.env['account.analytic.line'].create({
            'name': "Boleta " + str(rec.num_boleta),
            'account_id': rec.cuenta_analitica.id,
            'partner_id': rec.cliente.id,
            'date': rec.date,
            'amount': rec.costo_viaje,
            'unit_amount': 1,
            #'product_id': product_id.id,
            #'product_uom_id': product_id.uom_id.id,
        })

        return rec

    name = fields.Char("Consecutivo", tracking=True)
    date = fields.Date("Fecha Entrada", default=datetime.today(), tracking=True)
    placa = fields.Many2one("fleet.vehicle", string="Placa", tracking=True)
    cuenta_analitica = fields.Many2one("account.analytic.account", string="Cuenta A.", tracking=True)
    chofer = fields.Many2one("hr.employee", string="Chofer", tracking=True)
    ayudante1 = fields.Many2one("hr.employee", string="Ayudante 1", tracking=True)
    ayudante2 = fields.Many2one("hr.employee", string="Ayudante 2", tracking=True)
    num_boleta = fields.Char("Num. Boleta", tracking=True)
    cliente = fields.Many2one("res.partner", string="Cliente", tracking=True)
    ruta = fields.Many2one("boleta_ruta", string="Ruta", tracking=True)
    costo_viaje = fields.Float("Costo viaje")
    costo_viaticos = fields.Float("Costo viáticos")


class boleta_ruta(models.Model):
    _name = "boleta_ruta"
    _description = "boleta_ruta"

    name = fields.Char("Ruta")
    codigo = fields.Char("Código")
    #tipo_ruta = fields.Selection([('corta', 'Ruta Corta'), ('larga', 'Ruta Larga'), ('bcorta', 'Barco Corto'), ('blargo', 'Barco Largo'), ('otras', 'Otras rutas')], string="Tipo Ruta")
    costo_viaje = fields.Float("Costo viaje")
    costo_viaticos = fields.Float("Costo viáticos")