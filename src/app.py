import	hug

import	conf
from	route		import index

api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api, allow_origins=["*"]))

@hug.extend_api('')
def index_api():
	return [index]
