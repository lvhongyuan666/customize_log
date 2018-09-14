# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Pause(models.Model):
    _name = 'customize_log.pause'

    pause_name = fields.Many2one('customize_log.task', string='暂停时段')
    pause_start = fields.Datetime(string='暂停开始时间', readonly=True)
    pause_end = fields.Datetime(string='暂停结束时间', readonly=True)
    pause_kind = fields.Selection([('1', '已下班'), ('2', '处理紧急任务'), ('3', '其他')], string='暂停类型')
    pause_reason = fields.Text(string='暂停原因')

