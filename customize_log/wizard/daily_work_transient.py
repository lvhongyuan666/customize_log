# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api
from datetime import datetime, timedelta


class DailyWorkWizard(models.TransientModel):
    _name = 'customize_log.daily_work_wizard'
    _description = '默认生成当天日志'

    name_id = fields.Many2one('res.users', string='员工')
    time = fields.Date(default=fields.Date.today, string='日志时间')

    @api.multi
    def generate_daily_work(self):
        # 过滤开始时间等于选定时间,且最后修改人等于选定人员  2018-09-11 08:41:08 这里的time是时间模块time,而不是上面的字段
        res_data = self.env['customize_log.task'].search(['&', ('end_date', '<=', time.strftime('%Y-%m-%d 23:59:59')),
                                                          ('end_date', '>', time.strftime('%Y-%m-%d 00:00:00')),
                                                          ('state', '=', 'done'),
                                                          ('write_uid', '=', self.name_id.name)])

        # print(res_data) 过滤后的任务记录[]多个记录对象
        self.env['daily_work'].create({
            # 将这条记录的id赋值给新创建的记录的名字
            'name': self.name_id.id,
            'time': self.time,
            'task': [(4, r.id) for r in res_data],
        })
        return True


class CustomizeDailyWorkWizard(models.TransientModel):
    _name = 'customize_log.customize_daily_work'
    _description = '选择时间段生成日志'

    name_id = fields.Many2one('res.users', string='员工')
    start_time = fields.Datetime(default=fields.Datetime.now, string='开始时间')
    end_time = fields.Datetime(default=fields.Datetime.now, string='结束时间')

    _sql_constraints = [
        ('time_constraints',  'CHECK(start_time <= end_time)', "The end time is greater than the start time!"),
    ]

    @api.multi
    def customize_generate_daily_work(self):
        # 过滤符合条件的任务
        # print(self.start_time) 2018-09-21 00:45:53
        # fields.Datetime.from_string(self.start_time) 两种效果获取的值是一样的
        # start_time = fields.Datetime.from_string(self.start_time)+timedelta(hours=8) 2018-09-21 08:45:53

        res_data = self.env['customize_log.task'].search([('start_date', '>=', self.start_time),
                                                          ('end_date', '<=', self.end_time),
                                                          ('state', '=', 'done'),
                                                          ('write_uid', '=', self.name_id.name)
                                                          ])

        print(res_data)
        self.env['customize_daily_work'].create({
            # 将这条记录的id赋值给新创建的记录的名字
            'name': self.name_id.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'task_id': [(4, r.id) for r in res_data],
        })

        return True

