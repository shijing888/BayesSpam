
import jieba

class SplitWords:

	def __init__(self, content):
		self.content = content

	def get_word_list(self):
		res_list = list(jieba.cut(self.content))
		word_list = []
		for i in res_list:
			word_list.append(i.encode('utf-8'))
		return word_list

def main():
	content = '''
	毕业论文攻坚阶段，请保持手机畅通，经常查看邮件，随时和导师进行联系和沟通。随意，淡漠，不积极主动必定给自己的顺利毕业蒙上一层阴霾。
	'''
	word_list = SplitWords(content).get_word_list()
	print ('/'.join(word_list))

if __name__ == '__main__':
	main()

