# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SchoolEstablishmentWebServices(models.Model):

    _inherit = 'horanet.school.establishment'

    id_establishment = fields.Char(string='idEtablissement')

