import	hug

import	conf
from	route		import index

api = hug.API(__name__)

@hug.extend_api('')
def index_api():
	return [index]
