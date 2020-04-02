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

#from mycroft.client.enclosure.generic import EnclosureGeneric
from jarbas_utils.system import system_reboot, system_shutdown, ssh_enable, ssh_disable
from jarbas_utils import wait_for_exit_signal
from jarbas_utils.sound.pulse import PulseAudio
from jarbas_utils.log import LOG
from jarbas_utils.messagebus import get_mycroft_bus, Message

class EnclosureMycroftOS:

	def __init__(self):
		super().__init__()
		LOG.info('Setting up MycroftOS enclosure')
		self.bus = get_mycroft_bus()

		# Messagebus listeners
		self.bus.on("system.shutdown", self.handle_shutdown)
		self.bus.on("system.reboot", self.handle_reboot)
		self.bus.on("mycroft.volume.set", self.on_volume_set)
		self.bus.on("mycroft.volume.get", self.on_volume_get)
		self.bus.on("mycroft.volume.duck", self.on_volume_duck)
		self.bus.on("mycroft.volume.unduck", self.on_volume_unduck)

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

if __name__ == "__main__":
	EnclosureMycroftOS()
	wait_for_exit_signal()
