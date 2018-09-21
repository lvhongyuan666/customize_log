
{
    'name': "日志模块",
    'summary': "日志系统",
    'author': 'lhy',
    'website': "",
    'category': '',
    'version': '11.0.1.0.2',
    'depends': [
        'base', 'hr', 'web_editor', 'web',
    ],
    'data': [
        'security/task_security.xml',
        'security/ir.model.access.csv',
        'views/task_view.xml',
        'views/create_employee_from_user_view.xml',
        'views/pause_view.xml',
        'views/daily_work_view.xml',
        'wizard/daily_work_transient_view.xml',
        'report/print_daily_work_reports.xml',
        'report/print_daily_work_templates.xml',
        'wizard/pause_reason_transient_view.xml',
        'wizard/customize_daily_work_transient_view.xml',
        'views/customize_daily_work_view.xml',
        'report/print_customize_daily_work_templates.xml',
    ],
    'installable': True,
}
