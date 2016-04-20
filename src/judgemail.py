#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
from emailparser import EmailParser
from splitwords import SplitWords
from trainmodule import TrainModule

class JudgeMail:
	'''
	calculate the possibility of being a spam
	'''

	def __init__(self, mail_file, is_given_mail=False):
		self.mail_file = mail_file
		self.is_given_mail = is_given_mail

		self.train_module = TrainModule()

		self.P_SPAM = 0.5
		self.P_NORMAL = 1 - self.P_SPAM

		self.P_SPAM_WORD = 0.4

		self.P_IS_SPAM_LIMIT = 0.9

		self.train_module.set_dic_word_freq()

	def judge(self):
		mail_content = EmailParser(self.mail_file, self.is_given_mail).get_mail_content()

		res_list = SplitWords(mail_content).get_word_list()
		word_list = list(set(res_list))
		for i in \
[';', ':', ',', '.', '?', '!', '(', ')', ' ', '/', '@',\
'+', '-', '=', '*', '“', '”', \
 '；', '：', '，', '。', '？', '！', '（', '）', '　', '、']:
			if i in word_list:
				word_list.remove(i)

		word_freq = []
		for word in word_list:
			if word in self.train_module.dic_word_freq:
				p_w_n = self.train_module.dic_word_freq[word][0]
				p_w_s = self.train_module.dic_word_freq[word][1]
				p_s_w = p_w_s * self.P_SPAM / (p_w_s * self.P_SPAM + p_w_n * self.P_NORMAL)

				word_freq.append((word, p_s_w))
			else:
				word_freq.append((word, self.P_SPAM_WORD))

		word_freq_most = sorted(word_freq, key = lambda x:x[1], reverse=True)[:15]

		p = 1.0
		rest_p = 1.0
		k = 1.0
		for i in word_freq_most:
			print (i[0], i[1])
			k *= 1.0 / i[1] - 1

		p_spam = 1 / (1 + k)
		mail_type = ''
		if p_spam > self.P_IS_SPAM_LIMIT:
			mail_type = 'spam'
		else:
			mail_type = 'normal'

		self.train_module.update(mail_type, word_list)
		return p_spam

def main():
	fp = open(sys.argv[1], 'r')
	p = JudgeMail(fp, True).judge()
	fp.close()

	print ('SPAM: p = ', p)

if __name__ == '__main__':
	main()

