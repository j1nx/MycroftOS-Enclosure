#!/usr/bin/env python
##########################################################################
# framebuffer.py
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

from collections import namedtuple
from datetime import datetime

# Basic drawing to the framebuffer
Color = namedtuple('Color', ['red', 'green', 'blue'])
Screen = namedtuple('Screen', ['height', 'width'])

SCREEN = Screen(1080, 720)
BACKGROUND = Color(34, 167, 240)

FONT_PATH = 'NotoSansDisplay-Bold.ttf'

def fit_font(text, font_path, font_size):
	""" Brute force a good fontsize to make text fit screen. """
	font = ImageFont.truetype(font_path, font_size)
	w, h = font.getsize(text)
	while w < 0.9 * SCREEN.width:
		# iterate until the text size is just larger than the criteria
		font_size += 1
		font = ImageFont.truetype(font_path, font_size)
		w, h = font.getsize(text)

	return font

def write_fb(im, dev='/dev/fb0'):
	""" Write Image Object to framebuffer.
		TODO: Check memory mapping
	"""
	start_time = time.time()
	cols = []
	for j in range(im.size[1] - 1):
		for i in range(im.size[0]):
			R, G, B, A = im.getpixel((i, j))
			# Write color data in the correct order for the screen
			cols.append(struct.pack('BBBB', B, G, R, A))
	LOG.info('Row time: {}'.format(time.time() - start_time))
	with open(dev, 'wb') as f:
		color = [BACKGROUND.blue, BACKGROUND.green, BACKGROUND.red, 0]
		f.write(struct.pack('BBBB', *color) *
				((SCREEN.height - im.size[1]) // 2  * SCREEN.width))
		f.write(b''.join(cols))
		f.write(struct.pack('BBBB', *color) *
				((SCREEN.height - im.size[1]) // 2  * SCREEN.width))

		LOG.debug('Draw time: {}'.format(time.time() - start_time))

def draw_file(file_path, dev='/dev/fb0'):
	""" Writes a file directly to the framebuff device.
	Arguments:
		file_path (str): path to file to be drawn to frame buffer device
		dev (str): Optional framebuffer device to write to
	"""
	with open(file_path, 'rb') as img:
		with open(dev, 'wb') as fb:
			fb.write(img.read())