# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime


class ResPartner(models.Model):

    _inherit = 'res.partner'

    scholarship_ids = fields.One2many(string='School card', comodel_name='ecole.partner.school',
                                      inverse_name='partner_id')
    difference_age = fields.Boolean(string='Age', compute="_date_now", store=False)
    # school_certificate = fields.Binary(string='School certificate')

    # endregion


# fonction calcul age pour affichage onglet scolaire dans citoyens
    @api.one
    def _date_now(self):
        if self.birthdate_date:
            birth = fields.Date.from_string(self.birthdate_date)
            date_j = datetime.datetime.today()
            if ((date_j.year - birth.year) < 12) and ((date_j.year - birth.year) > 1):
                self.difference_age = True
        else:
            self.difference_age = True
