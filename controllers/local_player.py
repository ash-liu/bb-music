#!/usr/bin/env python
# coding: utf-8


import sys, os, time
import threading

import pygst
import gst, gtk, gobject


class Player_list:
	def __init__(self, list):
		self.list = list
		print self.list
		self.current = 0
		self.mode = 'normal'

	def get_next_song(self):
		if self.current < len(self.list):
			song = self.list[self.current]
			self.current += 1
		else :
			song = ''

		return song

	def get_prev_song(self):
		if self.current > 0:
			self.current -= 1
			song = self.list[self.current]
		else :
			song = ''

		return song

	def get_current(self):
		return self.current

	def get_current_song(self):
		return self.list[self.current]


class Player(threading.Thread):
	def __init__(self):
		self.player = gst.Pipeline("player")
		source = gst.element_factory_make("filesrc", "file-source")
		decoder = gst.element_factory_make("mad", "mp3-decoder")
		conv = gst.element_factory_make("audioconvert", "converter")
		sink = gst.element_factory_make("alsasink", "alsa-output")

		self.player.add(source, decoder, conv, sink)
		gst.element_link_many(source, decoder, conv, sink)

		self.state = 'null'
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)

		self.play_list = Player_list(['/home/root/simple-todo-read-only/mp3/ay.mp3', 
			                          '/home/root/simple-todo-read-only/mp3/hx.mp3',
			                          '/home/root/simple-todo-read-only/mp3/kxbsn.mp3'])

		threading.Thread.__init__(self)
		self.deamon = True

	def start_stop(self):
		if self.state == 'null':
			file_path = self.play_list.get_next_song()
			if os.path.isfile(file_path):
				print "play"
				self.state = 'play'
				self.player.get_by_name("file-source").set_property("location", file_path)
				self.player.set_state(gst.STATE_PLAYING)
			else:
				print "file not exist"
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
		print t
		if t == gst.MESSAGE_EOS:
			print "*****a song is over.*******"
			file_path = self.play_list.get_next_song()
			if os.path.isfile(file_path):
				print "play"
				self.state = 'play'
				self.player.set_state(gst.STATE_NULL)
				self.player.get_by_name("file-source").set_property("location", file_path)
				self.player.set_state(gst.STATE_PLAYING)
			else:
				print "file not exist"

		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			self.state = 'stop'
			err, debug = message.parse_error()
			print "Error: %s" % err, debug 


	def next_song(self):
		file_path = self.play_list.get_next_song()
		if os.path.isfile(file_path):
			print "play"
			self.state = 'play'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)
		else:
			print "file not exist"

		pass

	def prev_song(self):
		file_path = self.play_list.get_prev_song()
		if os.path.isfile(file_path):
			print "play"
			self.state = 'play'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)
		else:
			print "file not exist"
		pass

	def run(self):
		gtk.gdk.threads_init()
		gtk.main()
		pass

	def get_current_song(self):
		return self.play_list.get_current_song()



player = Player()
player.start()


if __name__ == '__main__' :
	player.start_stop()
