#!/usr/bin/env python
##########################################################################
# pulseaudio.py
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
import subprocess


def on_volume_set(self, message):
	self.muted = False
	self.set_pulse_volume(vol)

def on_volume_get(self, message):
	self.bus.emit(message.response(data={'percent': self.volume, 'muted': self.muted}))

def on_volume_duck(self, message):
	self.muted = True
	call(['pactl', 'set-sink-mute', '0', '1'])

def on_volume_unduck(self, message):
	self.muted = False
	call(['pactl', 'set-sink-mute', '0', '0'])