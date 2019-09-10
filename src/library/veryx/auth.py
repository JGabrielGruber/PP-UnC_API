import	json
import	jwt
import	os
from	falcon			import HTTP_403
from	model.usuario	import Usuario

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
				if content["level"] == level or level == "basic" or content["level"] == "admin":
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
				content		= jwt.decode(token.encode('utf8'), secret_key, algorithm='HS256')
				ids			= request.relative_uri.split('/')
				aluno_id	= Usuario.objects.get(id=ids[2]).materias.get(_id=ids[4]).turmas.get(_id=ids[6]).provas.get(_id=ids[8]).realizacoes.get(_id=ids[10]).aluno._id
				usuario_id	= Usuario.objects.get(id=ids[2]).email
				if content['level'] == "aluno":
					expiration	= datetime.strptime(content["token_expiration_date"], "%Y-%m-%d %H:%M:%S")
					if str(content['client_id']) == aluno_id and expiration >= datetime.now():
						response.append_header('locals', content)
						return True
				elif str(content['client_id']) == str(usuario_id) or content["level"] == "admin":
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
				print(request.relative_uri.split('/'))
				id		= Usuario.objects.get(id=request.relative_uri.split('/')[2]).email
				if str(content['client_id']) == str(id) or content["level"] == "admin":
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
