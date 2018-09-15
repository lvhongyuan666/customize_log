# -*- coding: utf-8 -*-
import time
from odoo import models, fields, api


class DailyWorkWizard(models.TransientModel):
    _name = 'customize_log.daily_work_wizard'

    name_id = fields.Many2one('res.users', string='员工')
    time = fields.Date(default=fields.Date.today, string='日志时间')

    @api.multi
    def generate_daily_work(self):
        # 过滤开始时间等于选定时间,且最后修改人等于选定人员  2018-09-11 08:41:08
        res_data = self.env['customize_log.task'].search(['&', ('end_date',  '<=', time.strftime('%Y-%m-%d 23:59:59')),
                                                          ('end_date',  '>', time.strftime('%Y-%m-%d 00:00:00')),
                                                          ('state', '=', 'done'),
                                                          ('write_uid', '=', self.name_id.name)])

        # print(res_data) 过滤后的任务记录[]多个记录对象
        self.env['daily_work'].create({
            # 将这条记录的id赋值给新创建的记录的名字
            'name': self.name_id.id,
            'time': fields.Date.today(),
            'task': [(4, r.id) for r in res_data],
        })
        return True



