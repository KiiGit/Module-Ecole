# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SchoolGradeWebServices(models.Model):

    _inherit = 'horanet.school.grade'

    id_class = fields.Char(string='idClasse')

