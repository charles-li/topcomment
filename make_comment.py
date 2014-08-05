

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


def comment(file_or_path=None, depth=5, type=['py']):
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
	print cf

if __name__=='__main__':
	comment()
