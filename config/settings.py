#!/usr/bin/env python
# coding: utf-8
import web

db = web.database(dbn='sqlite', db='/home/root/simple-todo-read-only/config/todo')

render = web.template.render('templates/', cache=False)

web.config.debug = True

config = web.storage(
    email='qichangxing@gmail.com',
    site_name = '任务跟踪',
    site_desc = '',
    static = '/static',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
