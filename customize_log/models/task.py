# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from odoo import models, fields, api


class Task(models.Model):
    _name = 'customize_log.task'

    # 只有在未激活状态下才可以编辑
    content = fields.Text(string='任务内容', states={'draft': [('readonly', False)]}, required=True, readonly=True)
    content_kind = fields.Selection([('regular', '日常工作'), ('chat', '部门间沟通'), ('emergency', '突发情况'), ('other', '其他')],
                                    string='内容类型')

    task_kind = fields.Selection([('view', '视图任务'), ('standard', '标准任务')], default='standard', string='任务类型')
    prestart_date = fields.Date(string='预计开始时间')
    preend_date = fields.Date(string='预计结束时间')
    # 任务所属部门,默认是当前部门
    task_department = fields.Many2one('hr.department', default=lambda self: self.env.user.employee_id.department_id,
                                      string='任务所属部门', readonly=True)
    state = fields.Selection([('draft', '未激活'), ('dealt', '待办理'), ('process', '进行中'), ('pause', '已暂停'),
                              ('done', '已完成'), ('cancel', '已取消')], string='任务状态', default='draft')
    user_id = fields.Many2one('hr.employee', default=lambda self: self.env.user.employee_id, string='任务发布人',
                              readonly=True)
    distribution = fields.Many2one('res.users', default=lambda self: self.env.uid, string='分配人')
    # 当个人任务的时候,隐藏执行人字段, 并将执行人默认值设为空
    executor = fields.Many2one('res.users', default=None, string='执行人')

    task_level = fields.Selection([('personal', '个人任务'), ('department', '部门任务'), ('company', '公司任务')], string='任务级别',
                                  default='personal', readonly=True)
    receive = fields.Boolean(string='可领取', default=False)

    start_date = fields.Datetime(string='任务产生时间', default=fields.Datetime.now)
    # digits = (6, 2)指定了浮点的精确度：4 是数字的总位数，而2是小数的位数。因此请注意，整数部分的位数最多是2位
    duration = fields.Float(string='预计持续时间', digits=(4, 2))
    end_date = fields.Datetime(string='任务结束时间', readonly=True)
    cancel_date = fields.Datetime(string='任务取消时间', readonly=True)
    image = fields.Html(string='工作截图')
    # 暂停任务模型对应字段
    pause_time = fields.One2many('customize_log.pause', 'pause_name', string='暂停时间')
    # 任务取消时展示的字段
    cancel_kind = fields.Selection([('1', '任务内容错误'), ('2', '任务临时取消'), ('3', '其他')], string='取消类型')
    cancel_reason = fields.Text(string='取消原因')

    # 添加一个dailywork(日志模型)相关字段
    daily_work = fields.Many2many('daily_work', string='日志')

    @api.multi
    def action_active_task(self):
        self.state = 'dealt'
        # print(time.strftime('%Y-%m-%d 23:59:59'))
        return True

    @api.multi
    def action_process(self):
        self.state = 'process'
        # self.receive = False 如果先改变可接收状态, 则普通用户无该记录的访问权限-->会弹出安全访问限制
        # 当任务为部门任务或公司任务时, 点击办理按钮,执行人变当前用户
        if self.task_level == 'department' or self.task_level == 'company':
            self.executor = self.env.user
            # 当前用户为执行人,该用户拥有这条记录的权限,然后在对状态进行改变
            self.receive = False
        return True

    @api.multi
    def action_stop_task(self):
        self.state = 'pause'
        # self表示当前的任务对象customize_log.task(165,)
        # print(self)
        # 表示暂停的对象 customize_log.pause() 'src_model': 'customize_log.task'
        # print(self.pause_time)

        # 在one2many字段赋值: 在many端添加一条数据
        # self.write({
        #     'pause_time': [(0, 0, {'pause_start': fields.Datetime.now()})]
        #
        # })
        return {
            'name': '暂停原因填写',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': False,
            'res_model': 'customize_log.pause_reason_wizard',
            'domain': [],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'task_id': self.id}

        }

    @api.multi
    def action_restart_task(self):
        self.state = 'process'
        restart_time = fields.Datetime.now()
        # 获取many端的模型对象,获取是暂停模型的所有数据对象 customize_log.pause(38, 39, 40)
        res_data = self.pause_time

        # 过滤符合条件的数据对象 条件:如果pause_end字段为空
        obj = res_data.filtered(lambda r: not r.pause_end)
        # print(obj)  # 符合条件的中一条数据对象customize_log.pause(39,)
        if obj:
            obj.pause_end = restart_time
        return True

    @api.multi
    def action_cancel_task(self):
        self.state = 'cancel'
        # 当点击任务取消按钮时,产生的时间赋值给任务完成时间
        task_cancel = fields.Datetime.now()
        self.cancel_date = task_cancel
        return True

    @api.multi
    def action_finish_task(self):
        self.state = 'done'
        # 当点击任务完成按钮时,产生的时间赋值给任务完成时间
        task_end = fields.Datetime.now()
        # print(task_end)
        self.end_date = task_end
        return True

    @api.multi
    def task_level_button_control(self):
        for r in self:
            if r.task_level == 'personal':
                r.task_level = 'department'
            elif r.task_level == 'department':
                if self.env.user.has_group('hr.group_hr_user'):
                    r.task_level = 'personal'
                if self.env.user.has_group('hr.group_hr_manager'):
                    r.task_level = 'company'

            elif r.task_level == 'company':
                r.task_level = 'personal'
