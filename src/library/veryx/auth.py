import	json
import	jwt
import	os
from	falcon					import HTTP_403

def authenticator(function):
	def wrapper(level="basic"):
		def authenticate(request, response, **kwargs):
			return function(request, response, level, **kwargs)
		return authenticate
	return wrapper

@authenticator
def basicAccess(request, response, level="basic", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()
			try:
				content	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				if content["level"] == level or level == "basic":
					response.append_header('locals', content)
					return True
				raise jwt.DecodeError()
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

@authenticator
def advancedAccess(request, response, level="empresa", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()

			try:
				content	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				id		= request.relative_uri.split('/')[-2]
				if str(content["client_id"]) == str(id) or content["level"] == level:
					content["id"]	= id
					response.append_header('locals', content)
					return True
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

@authenticator
def ownerAccess(request, response, level="basic", context=None, **kwargs):
	"""Token verification"""
	token = request.get_header('Authorization')
	if token:
		if token.split("Bearer ",1)[1]:
			token	= token.split("Bearer ",1)[1]

			secret_key	= getSecret()

			try:
				content	= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				id		= request.relative_uri.split('/')[-2]
				if str(content['client_id']) == str(id):
					response.append_header('locals', content)
					return True
			except jwt.DecodeError:
				response.status = HTTP_403
				return { "error" : "access_denied" }
		response.status = HTTP_403
		return { "error" : "access_denied" }
	response.status = HTTP_403
	return { "error" : "access_denied" }

def getSecret():
	if not os.path.exists('./.cache'):
		os.makedirs('./.cache')
	if os.path.exists('./.cache/secret.json'):
		with open('./.cache/secret.json', mode='rb') as privatefile:
			return	json.loads(privatefile.read())['secret']
	else:
		with open('./.cache/secret.json', mode='w') as file:
			file.write(json.dumps({ "secret" : cryptKey.newKey() }))
		getSecret()
