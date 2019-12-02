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
from mycroft.client.enclosure.generic import EnclosureGeneric

class EnclosureMycroftOS(EnclosureGeneric):

	def __init__(self):
		super().__init__()

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

	def on_volume_get(self, message):

	def on_volume_duck(self, message):

	def on_volume_unduck(self, message):


if __name__ == '__main__':
	enc = EnclosureMycroftOS()
	enc.run()
