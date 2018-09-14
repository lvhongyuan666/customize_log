# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PauseReasonWizard(models.TransientModel):
    _name = 'customize_log.pause_reason_wizard'

    pause_kind = fields.Selection([('1', '已下班'), ('2', '处理紧急任务'), ('3', '其他')], string='暂停类型')
    pause_reason = fields.Text(string='暂停原因')

    @api.multi
    def generate_pause_record(self):

        # 获取任务的id
        task_id = self.env.context.get('task_id', False)
        # 获取任务对象,给任务对象创建一条对应的暂停记录

        task_obj = self.env['customize_log.task'].browse(task_id)
        # print(task_obj)
        # 创建一条暂停记录
        task_obj.write({
            'pause_time': [(0, 0, {'pause_start': fields.Datetime.now(),
                                   'pause_kind': self.pause_kind,
                                   'pause_reason': self.pause_reason
                                   })]
        })

        return True

    @api.multi
    def state_action(self):
        # 根据上下文获取当前任务的id
        task_id = self.env.context.get('task_id', False)
        # 根据id,获取当前任务对象
        task_obj = self.env['customize_log.task'].browse(task_id)
        # 当用户点击取消时,恢复原来进行中状态
        task_obj.state = 'process'
        return True
