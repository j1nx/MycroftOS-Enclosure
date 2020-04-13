#!/usr/bin/env python
##########################################################################
# MycroftOS-Enclosure.py
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

import os
import sys

from mycroft.client.enclosure.generic import EnclosureGeneric
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG
from mycroft.api import is_paired


class MycroftOS_Enclosure(EnclosureGeneric):

	def __init__(self):
		super().__init__()
		LOG.info('Setting up MycroftOS enclosure')

		# OS administrative messages
		self.bus.on("system.shutdown", self.handle_shutdown)
		self.bus.on("system.reboot", self.handle_reboot)

		# Handle volume settings via PulseAudio
		self.bus.on("mycroft.volume.set", self.on_volume_set)
		self.bus.on("mycroft.volume.get", self.on_volume_get)
		self.bus.on("mycroft.volume.duck", self.on_volume_duck)
		self.bus.on("mycroft.volume.unduck", self.on_volume_unduck)
		
		# Interaction feedback
		self.bus.on("recognizer_loop:wakeword", self.indicate_listening)
		self.bus.on("recognizer_loop:record_begin", self.indicate_listening)
		self.bus.on("recognizer_loop:record_end", self.indicate_listening_done)

		self.bus.on("recognizer_loop:sleep", self.indicate_sleeping)
		self.bus.on("mycroft.awoken", self.indicate_waking)

		self.bus.on("recognizer_loop:audio_output_start", self.indicate_talking)
		self.bus.on("recognizer_loop:audio_output_end", self.indicate_talking_done)
		self.bus.on("mycroft.skill.handler.start", self.indicate_thinking)
		self.bus.on("mycroft.skill.handler.complete", self.indicate_thinking_done)

		# Visual indication that system is booting
		self.bus.on("mycroft.skills.initialized", self.indicate_booting_done)

		# Handle Device Ready
		self.bus.on('mycroft.ready', self.reset_screen)
		
		self.asleep = False
		self.indicate_booting()

	def indicate_booting(self):
		# Placeholder, override to start something during the bootup sequence

	def speak(self, utterance):
		LOG.info('Sending speak message...')
		self.bus.emit(Message('speak', data={'utterance': utterance}))

	def handle_shutdown(self, message):
		self.speak("Shutting down")
		system_shutdown()

	def handle_reboot(self, message):
		self.speak("rebooting")
		system_reboot()

	def on_volume_set(self, message):
		volume = message.data.get("volume", 50)
		assert 0 <= volume <= 100
		self.pulse.set_volume(volume)

	def on_volume_get(self, message):
		volume = self.pulse.get_volume()
		self.speak(volume)

	def on_volume_duck(self, message):
		self.pulse.mute_all()

	def on_volume_unduck(self, message):
		self.pulse.unmute_all()