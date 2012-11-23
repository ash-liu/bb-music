#!/usr/bin/env python
# coding: utf-8


import sys, os, time
import threading

import pygst
import gst, gtk, gobject

import urllib2
import simplejson


class Player_list:
	def __init__(self, list):
		self.list = list
		print self.list
		self.current = 0
		self.mode = 'normal'

		self.douban_url = "http://douban.fm/j/mine/playlist?type=s&sid=983357&channel=4&from=mainsite&r=23470fecb0"
		self.update_list(self.douban_url)


	def update_list(self, url):
		resp = urllib2.urlopen(url)
		html = resp.read()
		data = simplejson.loads(html)

		self.list = data['song']
		self.current = 0

	def get_next_song(self):
		if self.current < len(self.list):
			self.current += 1
			if self.current == len(self.list):
				self.update_list(self.douban_url)

			song = self.list[self.current]['url']


		return song

	def get_prev_song(self):
		return self.get_next_song()

	def get_current(self):
		return self.current

	def get_current_song(self):
		return self.list[self.current]

		

class Player(threading.Thread):
	def __init__(self):
		self.player = gst.Pipeline("player")
		source = gst.element_factory_make("souphttpsrc", "file-source")
		decoder = gst.element_factory_make("mad", "mp3-decoder")
		conv = gst.element_factory_make("audioconvert", "converter")
		volume = gst.element_factory_make("volume", "volume")
		sink = gst.element_factory_make("alsasink", "alsa-output")

		self.player.add(source, decoder, conv, volume, sink)
		gst.element_link_many(source, decoder, conv, volume, sink)

		self.state = 'null'
		
		self.bus = self.player.get_bus()
		self.bus.add_signal_watch()
		self.bus.connect("message", self.on_message)

		self.play_list = Player_list([])

		threading.Thread.__init__(self)
		self.deamon = True

		self.on_song_eos_handler = None


	def start_stop(self):
		if self.state == 'null':
			file_path = self.play_list.get_current_song()['url']
			print "play"
			self.state = 'play'
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)
			self.set_volume(60)
		elif self.state == 'pause':
			self.state = 'play'
			self.player.set_state(gst.STATE_PLAYING)
		elif self.state == 'play' :
			self.state = 'pause'
			self.player.set_state(gst.STATE_PAUSED)

		pass

	def get_state(self):
		return self.state

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			print "***** a song is over. *******"
			file_path = self.play_list.get_next_song()
			print "play"
			self.state = 'play'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)

			if self.on_song_eos_handler != None:
				self.on_song_eos_handler()
			else :
				print "on_song_eos_handler is None"

		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			self.state = 'stop'
			err, debug = message.parse_error()
			print "******Error: %s" % err, debug 

			# play again
			file_path = self.play_list.get_next_song()
			print "play"
			self.state = 'play'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)


	def next_song(self):
		file_path = self.play_list.get_next_song()
		print "play"
		self.state = 'play'
		self.player.set_state(gst.STATE_NULL)
		self.player.get_by_name("file-source").set_property("location", file_path)
		self.player.set_state(gst.STATE_PLAYING)

		pass

	def prev_song(self):
		file_path = self.play_list.get_prev_song()
		print "play"
		self.state = 'play'
		self.player.set_state(gst.STATE_NULL)
		self.player.get_by_name("file-source").set_property("location", file_path)
		self.player.set_state(gst.STATE_PLAYING)

		pass

	def set_volume(self, value):
		value = (value * 1.5) / 100.0
		self.player.get_by_name("volume").set_property("volume", value)


	def run(self):
		gtk.gdk.threads_init()
		gtk.main()
		pass

	def get_current_song(self):
		return self.play_list.get_current_song()

	def set_on_song_eos_handler(self, func):
		self.on_song_eos_handler = func


player = Player()
player.start()

if __name__ == '__main__' :
	player.start_stop()
