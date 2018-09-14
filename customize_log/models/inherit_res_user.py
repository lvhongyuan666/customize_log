# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UserInherit(models.Model):
    _inherit = 'res.users'

    employee_id = fields.Many2one('hr.employee',
                                  string='相关员工', auto_join=True,
                                  help='Employee-related data of the user')

    @api.model
    def create(self, vals):
        """This code is to create an employee while creating an user."""

        result = super(UserInherit, self).create(vals)
        result['employee_id'] = self.env['hr.employee'].sudo().create({'name': result['name'],
                                                                       'user_id': result['id'],
                                                                       'address_home_id': result['partner_id'].id})
        return result

