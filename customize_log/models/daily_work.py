# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DailyWork(models.Model):
    _name = 'daily_work'

    name = fields.Many2one('res.users', string='员工')
    time = fields.Date(default=fields.Date.today, string='日志时间')
    task = fields.Many2many('customize_log.task', string='任务')
