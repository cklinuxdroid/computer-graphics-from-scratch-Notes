#-*- coding: utf-8 -*-
#!python

#raster-01.py
from PIL import Image
import math

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y


def putPixel(pixels, x, y, color):
	"""
	The PutPixel() function.
	"""
	# canvas coordinate to screen coordinate
	x = screen_width / 2 + x
	y = screen_height / 2  - y 

	if x < 0 or x >= screen_height or y < 0 or y >= screen_height:
		return

	pixels[x, y] = color

def interpolate(i0, d0, i1, d1):
	if i0 == i1:
		return [d0]
	values = []
	a = (d1 - d0) * 1.0 / (i1 - i0)
	d = d0
	for i in xrange(i0,i1):
		values.append(d)
		d = d + a
	return values

def drawLine(p0, p1, color):
	dx = p1.x - p0.x
	dy = p1.y - p0.y

	if abs(dx) > abs(dy):
		if dx < 0:
			p0,p1 = p1,p0

		ys = interpolate(p0.x, p0.y, p1.x, p1.y)
		for x in xrange(p0.x,p1.x):
			putPixel(pixels, x, ys[(x - p0.x) | 0], color)
	else:
		if dy < 0:
			p0,p1 = p1,p0

		xs = interpolate(p0.y, p0.x, p1.y, p1.x)
		for y in xrange(p0.y,p1.y):
			putPixel(pixels, xs[(y - p0.y) | 0], y, color)


def drawWireframeTriangle(p0, p1, p2, color):
	drawLine(p0, p1, color)
	drawLine(p1, p2, color)
	drawLine(p2, p0, color)

def drawFilledTriangle(p0, p1, p2, color):
	x0,y0 = p0.x,p0.y
	x1,y1 = p1.x,p1.y
	x2,y2 = p2.x,p2.y

	if y1 < y0: p0, p1 = p1, p0
	if y2 < y0: p0, p2 = p2, p0
	if y2 < y1: p1, p2 = p2, p1

	x01 = interpolate(y0, x0, y1, x1)
	x12 = interpolate(y1, x1, y2, x2)
	x02 = interpolate(y0, x0, y2, x2)

	del x01[-1]
	x012 = x01 + x12

	m = len(x02)/2 | 0
	if x02[m] < x012[m]:
		x_left = x02
		x_right = x012
	else:
		x_left = x012
		x_right = x02
		
	# int to use for in range
	x_left = [int(x) for x in x_left]
	x_right = [int(x) for x in x_right]


	for y in xrange(y0, y2-1):
		for x in xrange(x_left[y - y0], x_right[y - y0]):
			putPixel(pixels, x, y, color)


screen_width = 600
screen_height = 600
background_color = (255, 255, 255)

p0 = Point(-200, -250)
p1 = Point(200, 50)
p2 = Point(20, 250)


image = Image.new("RGBA", (screen_width, screen_height), background_color)
pixels = image.load()

drawFilledTriangle(p0, p1, p2, (0,255,0))
drawWireframeTriangle(p0, p1, p2, (0,0,0))
image.save("raster02.png")
