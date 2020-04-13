#!/usr/bin/env python
##########################################################################
# services.py
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


def ssh_enable():
	# Permanently allow SSH access
	subprocess.call('sudo systemctl enable ssh.service', shell=True)
	subprocess.call('sudo systemctl start ssh.service', shell=True)

def ssh_disable():
	# Permanently block SSH access from the outside
	subprocess.call('sudo systemctl stop ssh.service', shell=True)
	subprocess.call('sudo systemctl disable ssh.service', shell=True)