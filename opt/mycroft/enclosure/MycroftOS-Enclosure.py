#!/usr/bin/env python
##########################################################################
# MycroftOS-Enclosure.py
#
# Copyright 2019, j1nx.nl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################

import os, sys
from subprocess import call, check_output, CalledProcessError
from mycroft.client.enclosure.generic import EnclosureGeneric

class EnclosureMycroftOS(EnclosureGeneric):

	def __init__(self):
		super().__init__()

		# Volume control
		self.volume = 0.6
		self.muted = False

		# Messagebus listeners
		self.bus.on("system.shutdown", self.handle_shutdown)
		self.bus.on("system.reboot", self.handle_reboot)
		self.bus.on("mycroft.volume.set", self.on_volume_set)
		self.bus.on("mycroft.volume.get", self.on_volume_get)
		self.bus.on("mycroft.volume.duck", self.on_volume_duck)
		self.bus.on("mycroft.volume.unduck", self.on_volume_unduck)

	def handle_shutdown(self, message):
		os.system("shutdown --poweroff now")

	def handle_reboot(self, message):
		os.system("shutdown --reboot now")

	def on_volume_set(self, message):
		""" Set volume level by percentage"""
		vol = message.data.get("percent", 0.5)
		self.muted = False
		call(['pactl', 'set-sink-volume', '0', 'vol'])

	def on_volume_get(self, message):
		""" Handle request for current volume. """
		self.bus.emit(message.response(data={'percent': self.volume, 'muted': self.muted}))

	def on_volume_duck(self, message):
		""" Handle ducking event by muting. """
		self.muted = True
		self.mute_pulseaudio()

	def on_volume_unduck(self, message):
		""" Handle ducking event by unmuting. """
                self.muted = True
                self.unmute_pulseaudio()

	def mute_pulseaudio(self):
		"""Mutes pulseaudio volume"""
		call(['pactl', 'set-sink-mute', '0', '1'])

	def unmute_pulseaudio(self):
		"""Resets pulseaudio volume to max"""
		call(['pactl', 'set-sink-mute', '0', '0'])

if __name__ == '__main__':
	enc = EnclosureMycroftOS()
	enc.run()
