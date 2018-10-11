# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaskWizard(models.TransientModel):
    _name = 'customize_log.task_wizard'
    _description = '按部门查看员工任务'

    start_date = fields.Datetime(string='开始日期')
    end_date = fields.Datetime(string='结束日期')

    @api.multi
    def customize_generate_task(self):
        # 过滤掉状态为取消和未激活的任务
        res_data = self.env['customize_log.task'].search([('start_date', '>=', self.start_date),
                                                          ('start_date', '<=', self.end_date),
                                                          ('state', 'not in', ['draft', 'cancel'])
                                                          ])
        return {
            'name': '员工任务状态',
            'view_type': 'form',
            'view_mode': 'tree',
            'view_id': self.env.ref('customize_log.customize_log_task_wizard_view_tree').id,
            'res_model': 'customize_log.task',
            'domain': [('id', 'in', res_data.ids)],
            'type': 'ir.actions.act_window',
            'search_view_id': self.env.ref('customize_log.customize_log_task_wizard_view_search').id,
            'context': {'search_default_by_department': 1},
        }

