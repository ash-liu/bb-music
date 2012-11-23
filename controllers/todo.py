#!/usr/bin/env python
# coding: utf-8
import web

from config import settings
# from local_player import player
from douban_player import player

import simplejson
from threading import Event

render = settings.render

evt = Event()

'''  '''
def on_song_eos_handler():
    print "in on_song_eos_handler"
    evt.set()
    evt.clear()

class Index:
    ''' main page '''
    def GET(self):
        player.set_on_song_eos_handler(on_song_eos_handler)
        song = player.get_current_song()
        return render.index(song)


class Play:
    ''' play the music '''
    def GET(self):
        # do play
        print "play"
        if player.get_state() == 'null' or player.get_state() == 'pause' :
            player.start_stop()
        else :
            print "has been play"
        # raise web.seeother('/')
        web.header('Content-Type', 'application/json') 
        return simplejson.dumps(player.get_current_song())


class Pause:
    ''' pause the musci '''
    def GET(self):
        # do pause
        print "pause"
        if player.get_state() == 'play':
            player.start_stop()
        else :
            print "has been pause"

        # web.header('Content-Type', 'application/json') 
        # return simplejson.dumps(player.get_current_song())

class Next:
    ''' next song '''
    def GET(self):
        # do next
        print "next"
        player.next_song()

        on_song_eos_handler()

        # web.header('Content-Type', 'application/json') 
        # return simplejson.dumps(player.get_current_song())

class Prev:
    ''' prev song '''
    def GET(self):
        print "prev"
        player.prev_song()
        
        on_song_eos_handler()

        # web.header('Content-Type', 'application/json') 
        # return simplejson.dumps(player.get_current_song())

class Volume:
    ''' set the voice '''
    def GET(self):
        user_data = web.input()
        value = user_data.get('value', 60)

        player.set_volume(int(value))

        print "set voice :" + value


class Sync:
    ''' long connect for sync client info '''
    def GET(self):
        print "call sync"
        evt.wait()
        print "sync return !!!!!!"
        web.header('Content-Type', 'application/json') 
        return simplejson.dumps(player.get_current_song())

class Sync_test:
    def GET(self):
        on_song_eos_handler()
