

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
	last_updated_on = cf.get('file_specific', 'last updated')
	file_name_on = cf.get('file_specific', 'file name')

	res = dict(file_type=file_type, copyright=copyright, Author=Author,
			   Email=Email, last_updated_on=last_updated_on,
			   file_name_on=file_name_on)
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

	### traverse from file_or_path in depth to make top comment 
	### to each type of files in the parameter type
	for each_type in file_type:
		comment_msg = build_comment_msg(cf, each_type)
		comment_on(file_or_path, depth, each_type, comment_msg)

	return 

def comment_on(file_or_path, depth, each_type, comment_msg):
	'''
	A lowwer API for comment func
	'''
	import os
	import fileinput

	temp_depth = depth
	for root, dirs, files in os.walk(file_or_path):
		# files = os.path.join(root, files)
		for each_file in files:
			each_file = os.path.join(root, each_file)
			if '.' not in each_file or each_type not in each_file:
				continue
			else:
				flag = True
				for line in fileinput.input(each_file, inplace=1):
					if flag:
						print comment_msg
						print line,
						flag = False
					else:
						print line,
	return

def build_comment_msg(cf, each_type):
	'''
	Build cooment msg according to the correspond file type;
	'''
	msg = ''
	for term in cf:
		msg += (term + ': ' + cf[term] + '\n')

	return msg

if __name__=='__main__':
	cf = parse_conf()
	each_type = 'py'
	msg = build_comment_msg(cf, each_type)

	print msg
