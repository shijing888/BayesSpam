#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re

class SplitWords:
	'''
	首先通过当前目录下的词典建立字典树
	通过正则表达式分解邮件中的英文单词和汉字
	然后逐字检测可否组成字典中存在的单词或词组以达到简单的分词效果
	'''

	def __init__(self, content):
		self.REGEX = re.compile(r'[\w-]+|[\x80-\xff]{3}')
		self.content = content

	#读入字典，默认是当前目录的words.txt，也可自己传入位置参数
	def init_wordslist(self, fn = r'./words.txt'):
		f = open(fn)
		lines = sorted(f.readlines())
		f.close()
		return lines

	#字典树
	def words_to_trie(self):
		wordslist = self.init_wordslist()
		d = {}
		for word in wordslist:
			ref = d
			chars = self.REGEX.findall(word)
			for char in chars:
				ref[char] = ref.has_key(char) and ref[char] or {}
				ref = ref[char]
		return d

	def search_in_trie(self, chars, trie, res):
		'''
		逐字检索已经拆分为英文单词或单个汉字的邮件并在字典中查找最长匹配的词语
		'''

		ref = trie
		index = 0
		temp = ''
		count = 0
		for char in chars:
			if ref.has_key(char):
				temp += char
				count += 1
				ref = ref[char]
				index += 1
			else:
				if temp != 0:                                #表示上一个单词已经分离出
					res.append(temp)
					temp = ''
					count = 0
				if index == 0:                               #字典中没有以上一个char结尾的单词
					index = 1
					res.append(char)
				try:
					chars = chars[index:]
					self.search_in_trie(chars, trie, res)
				except:
					pass
				break
		if count != 0:                                       #最后一个词
			res.append(temp);

	def get_word_list(self):
		res = []
		chars = self.REGEX.findall(self.content)
		trie = self.words_to_trie()
		self.search_in_trie(chars, trie, res)
		res = list(set(res))
		return res

def main():
	content = '''
	毕业论文攻坚阶段，请保持手机畅通，经常查看邮件，随时和导师进行联系和沟通。随意，淡漠，不积极主动必定给自己的顺利毕业蒙上一层阴霾。
	'''
	word_list = SplitWords(content).get_word_list()
	print ('/'.join(word_list))

if __name__ == '__main__':
	main()

