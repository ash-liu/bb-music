#!/usr/bin/env python
# coding: utf-8


import sys, os, time

import pygst
import gst


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
			song = self.list[self.current]
			self.current -= 1
		else :
			song = ''

		return song

	def get_current(self):
		return self.current


class Player:
	def __init__(self):
		self.player = gst.Pipeline("player")
		source = gst.element_factory_make("filesrc", "file-source")
		decoder = gst.element_factory_make("mad", "mp3-decoder")
		conv = gst.element_factory_make("audioconvert", "converter")
		sink = gst.element_factory_make("alsasink", "alsa-output")

		self.player.add(source, decoder, conv, sink)
		gst.element_link_many(source, decoder, conv, sink)

		self.state = 'stop'
		
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.on_message)

		self.play_list = Player_list(['/home/root/simple-todo-read-only/mp3/ay.mp3', 
			                          '/home/root/simple-todo-read-only/mp3/hx.mp3',
			                          '/home/root/simple-todo-read-only/mp3/kxbsn.mp3'])

	def start_stop(self):
		if self.state == 'stop':
			file_path = self.play_list.get_next_song()
			if os.path.isfile(file_path):
				print "start"
				self.state = 'start'
				self.player.get_by_name("file-source").set_property("location", file_path)
				self.player.set_state(gst.STATE_PLAYING)
			else:
				print "file not exist"
		else :
			self.state = 'stop'
			self.player.set_state(gst.STATE_NULL)

		pass

	def get_state(self):
		return self.state

	def on_message(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			file_path = self.play_list.get_next_song()
			if os.path.isfile(file_path):
				print "start"
				self.state = 'start'
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
			print "start"
			self.state = 'start'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)
		else:
			print "file not exist"

		pass

	def prev_song(self):
		file_path = self.play_list.get_prev_song()
		if os.path.isfile(file_path):
			print "start"
			self.state = 'start'
			self.player.set_state(gst.STATE_NULL)
			self.player.get_by_name("file-source").set_property("location", file_path)
			self.player.set_state(gst.STATE_PLAYING)
		else:
			print "file not exist"
		pass

mp3_player = Player()

if __name__ == '__main__' :
	mp3_player.start_stop()
	while 1:
		time.sleep(1)