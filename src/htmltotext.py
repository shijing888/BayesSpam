# -*- coding: utf-8 -*-

from html import parser

class _MyHTMLParser(parser):

	def __init__(self):
# 		parser.__init__(self)
		self.text = ''
		self.hide_output = False

	def handle_starttag(self, tag, attrs):
		if tag in ('script','style'):
			self.hide_output = True

	def handle_endtag(self, tag):
		if tag in ('script','style'):
			self.hide_output = False

	def handle_data(self, data):
		if data and not self.hide_output:
			self.text += data

	def get_text(self):
		return self.text

class HTMLToText():

	"""
	extract plain text from a html document
	"""

	def __init__(self, html):
		self.html = html
		self.parser = _MyHTMLParser()

	def get_text(self):
		self.parser.feed(self.html)
		self.parser.close()
		return self.parser.get_text()

import sys

def main():
	fp = open(sys.argv[1], 'r')
	s = ''.join(fp.readlines())
	fp.close()
	s = HTMLToText(s.decode('utf-8')).get_text().encode('utf-8')
	print (s)

if __name__ == '__main__':
	main()

