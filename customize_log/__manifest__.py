
{
    'name': "日志模块",
    'summary': "日志系统",
    'author': 'lhy',
    'website': "",
    'category': '',
    'description': """

功能
=======

* 图文记录每一条工作任务
* 按天打印/自定义时间打印工作任务为pdf格式
* 按部门查看员工的工作进度情况

    """,
    'version': '11.0.1.0.2',
    'depends': [
        'base', 'hr', 'web_editor', 'web',
    ],
    'data': [
        'security/task_security.xml',
        'security/ir.model.access.csv',
        'views/task_views.xml',
        'views/pause_views.xml',
        'views/daily_work_views.xml',
        'wizard/daily_work_transient_views.xml',
        'report/print_daily_work_reports.xml',
        'report/print_daily_work_templates.xml',
        'wizard/pause_reason_transient_views.xml',
        'wizard/customize_daily_work_transient_views.xml',
        'views/customize_daily_work_views.xml',
        'report/print_customize_daily_work_templates.xml',
        'wizard/task_transient_views.xml',
    ],
    'installable': True,
}
