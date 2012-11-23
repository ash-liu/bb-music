#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',                    pre_fix + 'todo.Index',
    '/play',                pre_fix + 'todo.Play',
    '/pause',               pre_fix + 'todo.Pause',
    '/next',                pre_fix + 'todo.Next',
    '/prev',                pre_fix + 'todo.Prev',
    '/volume',              pre_fix + 'todo.Volume',
    '/sync',                pre_fix + 'todo.Sync',
    '/sync_test',           pre_fix + 'todo.Sync_test',
)
