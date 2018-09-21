# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DailyWork(models.Model):
    _name = 'daily_work'
    _description = '默认生成当天日志'

    name = fields.Many2one('res.users', string='员工')
    time = fields.Date(default=fields.Date.today, string='日志时间')
    task = fields.Many2many('customize_log.task', string='任务')


class CustomizeDailyWork(models.Model):
    _name = 'customize_daily_work'
    _description = '自定义生成日志时间'

    name = fields.Many2one('res.users', string='员工')
    start_time = fields.Datetime(string='开始时间')
    end_time = fields.Datetime(string='结束时间')
    task_id = fields.Many2many('customize_log.task', string='任务')
