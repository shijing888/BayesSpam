#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import re
import collections
from splitwords import SplitWords
#from splitwords_trie import SplitWords


class TrainModule:
	"""
		use given mails to train the module
	"""

	def __init__(self):
		self.wordlist = {'normal' : [], 'spam' : []}
		self.mail_count = {'normal' : 0, 'spam' : 0}
		self.dic_word_freq = {} # { 'word' : [0.1, 0.002], 'text' : [0.2, 0.001], ... }

		self.PRE_DEFINED_WORD_FREQ = 0.0001
		self.WORD_FREQ_FILE = '../data/tmp/freq_file.txt'

	def build_word_list(self, mail_dir):
		for dirt in os.listdir(mail_dir): # 'normal', 'spam'
			d = mail_dir + '/' + dirt + '/'
			print ('scanning directory: ', d)
			for filename in os.listdir(d):
				fp = open(d + filename).read()
				mail_content = fp[fp.index('\n\n')::]

				try:
					mail_content = mail_content.encode('utf-8')
				except:
					import sys
					print >> sys.stderr, 'ERROR: ', filename
					continue

# 				mail_content = re.sub('\s+', ' ', mail_content)
				res_list = SplitWords(mail_content).get_word_list()
				word_list = list(set(res_list))
				self.wordlist[dirt].extend(word_list)
				self.mail_count[dirt] += 1

	def calc_word_freq(self, mail_type):
		counter = collections.Counter(self.wordlist[mail_type])
		dic = collections.defaultdict(list)
		for word in list(counter):
			dic[word].append(counter[word])

		for key in dic:
			dic[key][0] *= 1.0 / self.mail_count[mail_type]

		return dic

	def build_freq_dict(self):
		print ('building word frequency dict...')
		self.build_word_list('../data')

		dic_word_freq_in_normal = self.calc_word_freq('normal')
		dic_word_freq_in_spam = self.calc_word_freq('spam')

		dic_word_freq = dic_word_freq_in_normal

		for key in dic_word_freq_in_spam:
			if key not in dic_word_freq:
				dic_word_freq[key].append(self.PRE_DEFINED_WORD_FREQ)
			dic_word_freq[key].append(dic_word_freq_in_spam[key][0])

		for key in dic_word_freq:
			if len(dic_word_freq[key]) == 1:
				dic_word_freq[key].append(self.PRE_DEFINED_WORD_FREQ)

		self.dic_word_freq = dic_word_freq

	def write_freq_file(self):
		print ('writing freq file...')

		dic_freq = self.dic_word_freq
		fp = open(self.WORD_FREQ_FILE, 'w')
		
		fp.write(str(self.mail_count['normal']) + ' ')
		fp.write(str(self.mail_count['spam']) + '\n')

		for key in dic_freq:
			fp.write(key.tostring())
			for v in dic_freq[key]:
				fp.write(' ' + str(v))
			fp.write('\n')

		fp.close()

	def read_freq_file(self):
		if not os.path.isfile(self.WORD_FREQ_FILE):
			return False

		print ('reading freq file...')

		fp = open(self.WORD_FREQ_FILE, 'r')
		word_freq_list = {}

		for line in fp.readlines():
			linelist = line.strip('\n').split(' ')

			if len(linelist) == 2:
				self.mail_count['normal'] = int(linelist[0])
				self.mail_count['spam'] = int(linelist[1])
			else:
				word_freq = { linelist[0] : [ float(linelist[1]), float(linelist[2]) ] }
				word_freq_list.update(word_freq)

		self.dic_word_freq =  word_freq_list
		fp.close()
		return True

	def set_dic_word_freq(self):
		if not self.read_freq_file():
			self.build_freq_dict()
			self.write_freq_file()

	def update(self, mail_type, word_list):
		if mail_type == 'normal':
			mt = 0
		else:
			mt = 1

		for word in word_list:
			if word not in self.dic_word_freq:
				self.dic_word_freq[word] = [ self.PRE_DEFINED_WORD_FREQ, self.PRE_DEFINED_WORD_FREQ ]
				self.dic_word_freq[word][mt] = 1.0 / (self.mail_count[mail_type] + 1)
			else:
				if self.dic_word_freq[word][mt] == self.PRE_DEFINED_WORD_FREQ:
					self.dic_word_freq[word][mt] = 1.0 / (self.mail_count[mail_type] + 1)
				else:
					self.dic_word_freq[word][mt] = \
				(1 + self.dic_word_freq[word][mt] * self.mail_count[mail_type]) / (self.mail_count[mail_type] + 1)

		self.mail_count[mail_type] += 1

import sys

def main():
	TrainModule().set_dic_word_freq()

if __name__ == '__main__':
	main()

