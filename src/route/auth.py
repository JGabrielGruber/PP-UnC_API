import	hug

from	controller		import auth
from	library.veryx	import auth as veryx

@hug.get('/token', requires=veryx.basicAccess(), version=1)
def get_data(response):
	return auth.getData(response)

@hug.post('/token', version=1)
def get_token(
	grant_type: hug.types.text,
	client_id: hug.types.number,
	client_secret: hug.types.text,
	response
):
	return auth.getToken(response, grant_type, client_id, client_secret)
