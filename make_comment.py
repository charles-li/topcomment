

import os


def parse_conf():
	'''
	Parse the common.conf config file.
	'''
	import ConfigParser
	cf = ConfigParser.ConfigParser()
	cf.read('common.conf')

	file_type = cf.get('file_type', 'type')
	copyright = cf.get('common_info', 'copyright')
	Author = cf.get('common_info', 'Author')
	Email = cf.get('common_info', 'Email')
	last_updated = cf.get('file_specific', 'last_updated')
	file_name = cf.get('file_specific', 'file_name')

	res = dict(type=file_type, copyright=copyright, Author=Author,
			   Email=Email, last_updated=last_updated,
			   file_name=file_name)
	return res


def comment(file_or_path=None, depth=5, file_type=['py']):
	'''
	Traverse from file_or_path in depth, and which type of files
	you wanna make comment.
	parameters details:
	file_or_path : if ommited, start from the current path where
				   the program is started;
	depth: maximum 5;
	type: support .py, .cpp, .c, .html, .js
	'''
	### parse the config file: common.conf
	cf = parse_conf()
	# print cf
	# import pdb
	# pdb.set_trace()
	### traverse from file_or_path in depth to make top comment 
	### to each type of files in the parameter type
	for each_type in file_type:
		comment_msg = build_direct_msg(cf, each_type)
		if not comment_msg:
			continue
		comment_on(file_or_path, depth, each_type, comment_msg, cf)

	return 

def comment_on(file_or_path, depth, each_type, comment_msg, cf):
	'''
	A lowwer API for comment func
	'''
	import fileinput
	temp_depth = depth

	for root, dirs, files in os.walk(file_or_path):
		# files = os.path.join(root, files)
		for each_file in files:
			# import pdb
			# pdb.set_trace()
			temp_comment_msg = comment_msg
			each_file = os.path.join(root, each_file)
			if '.' not in each_file or each_type != each_file.split('\\')[-1].split('.')[-1]:
				continue
			else:
				temp_comment_msg = add_specific_comment(temp_comment_msg, each_file, each_type, cf)
				flag = True
				f = fileinput.input(each_file, inplace=1)
				for line in f:
					if flag:
						print temp_comment_msg
						print line,
						flag = False
					else:
						print line,
				f.close()
	return

def build_direct_msg(cf, each_type):
	'''
	Build cooment msg according to the correspond file type;
	'''
	msg = ''
	direct = ['copyright', 'Author', 'Email']

	### if the file type is not supported.
	if each_type not in cf['type']:
		return False
	### build the comment way.
	if each_type == 'py':
		msg += "'''\n"
		# direct comment from common.conf
		for term in cf:
			if term in direct:
				msg += ('\t' + term + ': ' + cf[term] + '\n')
		# msg += "'''\n"
	if each_type in ['c', 'cpp', 'js']:
		msg += "/***********\n"
		# direct comment from common.conf
		for term in cf:
			if term in direct:
				msg += ('\t' + term + ': ' + cf[term] + '\n')
		# msg += "'''\n"
	return msg

def add_specific_comment(comment_msg, each_file, each_type, cf):
	'''
	Add specific comment information on comment_msg.
	Include filename, last modified time and so on.
	'''
	specific_comment = ['last_updated', 'file_name']
	
	if cf['last_updated'] == 'on':
		from time import ctime	
		m_time = os.stat(each_file).st_mtime
		m_time = ctime(m_time)
		comment_msg += ('\t' + 'last_updated' + ': ' + m_time + '\n')	
	if cf['file_name'] == 'on':
		comment_msg += ('\t' + 'file_name' + ': ' + each_file.split('/')[-1] + '\n')
	if each_type == 'py':
		comment_msg += "'''\n"
	elif each_type in ['c', 'cpp', 'js']:
		comment_msg += "****************/\n"
	else:
		pass
	return comment_msg

if __name__=='__main__':
	cf = parse_conf()
	# print cf

	each_type = 'py'
	msg = build_direct_msg(cf, each_type)

	print msg
