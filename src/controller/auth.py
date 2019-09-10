import	json
import	jwt
import	os
import	smtplib

from	email.message			import EmailMessage
from	email.headerregistry	import Address
from	email.utils				import make_msgid
from	falcon					import HTTP_400, HTTP_403, HTTP_502
from	datetime				import datetime, timedelta

from	library.cryption	import	cryptKey
from	conf				import	db_auth, db_data
from	model.usuario		import	Usuario
from	model.login			import	Login

# TODO: Implementar criação de token para aluno com base na realização que ele irá fazer, e também, com base na data que ele poderá usar este token para acessar esta prova
#		O id da realização dele e da prova não devem estr presente na URL
#		Se for o caso, implementar junto no token, então, passar para as funções

def setAuth(response, data, level="basic"):
	"""Create a new login, with the client_id and the encrypted client_secret"""
	try:
		hash			= cryptKey.newKey()
		senha			= cryptKey.encryptContent(data["senha"], hash)
		data["hash"]	= hash
		data.pop("senha")
		login			= Login(**data)
		login.save()
		return senha
	except Exception as e:
		print(e)
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getAuth(response, client_id, client_secret):
	"""Verify if the login exists"""
	try:
		auths	= json.loads(Login.objects.get(email=client_id).to_json())
		datas	= False
		level	= auths['level']
		datas	= json.loads(Usuario.objects.get(email=client_id).to_json())
		if auths and datas:
			if client_secret == cryptKey.decryptContent(datas['senha'], auths['hash']):
				return level
	except Exception as e:
		return False

def getToken(response, grant_type, client_id, client_secret):
	"""Returns a token for an existing client"""
	if grant_type == "client_credentials":
		secret_key	= getSecret()

		level	= getAuth(response, client_id, client_secret)
		if level:
			return {
				"access_token": jwt.encode({
							"client_id"	: client_id,
							"level"		: level
						}, secret_key, algorithm='HS256'
					).decode('utf8'),
				"token_type": "bearer",
			}
		response.status	= HTTP_400
		return { "error": "invalid_client" }
	response.status	= HTTP_400
	return { "error": "unsupported_grant_type" }

def updateAuth(response, client_id, client_secret, token, level="basic"):
	try:
		content	= jwt.decode(token.encode('utf8'), getSecret(), algorithm='HS256')
		expiration = datetime.strptime(content["token_expiration_date"], "%Y-%m-%d %H:%M:%S")
		if client_id == content['client_id']:
			if expiration >= datetime.now():
				return setAuth(response, client_id, client_secret, level)
	except jwt.DecodeError:
		response.status = HTTP_400
		return { "error": "invalid_client" }

def removeAuth(response, client_id):
	"""Remove the login"""
	locals		= eval(response.get_header("locals"))
	level		= locals['level']
	client_id	= locals['client_id']
	try:
			Login.objects.get(email=client_id).delete()
			return
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def sendReset(response, title, sender, receiver):
	token = jwt.encode({
			"client_id": receiver['client_id'],
			"token_expiration_date": format(datetime.now() + timedelta(hours=1), "%Y-%m-%d %H:%M:%S")
		}, getSecret(), algorithm="HS256"
	).decode('utf8')
	link = "https://127.0.0.1/reset_password?token=" + token
	msg = EmailMessage()
	msg['Subject'] = title
	msg['From'] = Address(sender['name'], sender['client_id'], sender['email'])
	msg['To'] = (Address(receiver['name'], str(receiver['client_id']), receiver['email']))
	content = """\
	Olá,

	Vimos que esqueceu sua senha, relaxa, com tanta coisa para lembra, é normal.
	Use este link[1] para poder alterar a mesma. Ele irá expirar em breve!

	[1]{0}

	Este é um email automático, não o responda!
	"""
	msg.set_content(content.format(link))

	asparagus_cid = make_msgid()

	content = """\
	<html>
	  <head></head>
	  <body>
		<p>Olá,</p>
		<pVimos que esqueceu sua senha, relaxa, com tanta coisa para lembra, é normal.</br>
		Use este <a href="{0}">link</a> para poder alterar a mesma. Ele irá expirar em breve!</p>
		<p>Este é um email automático, não o responda!</p>
	  </body>
	</html>
	""".format(link, asparagus_cid=asparagus_cid[1:-1])

	msg.add_alternative(content, subtype='html')

	try:
		with smtplib.SMTP('localhost') as s:
			s.send_message(msg)
			return ""
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

	return ""

def sendToken(response, title, sender, receiver, data):
	expiration	= format(datetime.now() + timedelta(minutes=receiver['minutes']), "%Y-%m-%d %H:%M:%S")
	token = jwt.encode({
			"client_id": receiver['client_id'],
			"token_expiration_date": expiration,
			"data": data,
			"level": receiver['level']
		}, getSecret(), algorithm="HS256"
	).decode('utf8')
	link = "https://127.0.0.1/realizarProva?token=" + token
	msg = EmailMessage()
	msg['Subject'] = title
	msg['From'] = Address(sender['name'], sender['client_id'], sender['email'])
	msg['To'] = (Address(receiver['name'], str(receiver['client_id']), receiver['email']))
	content = """\
	Olá,

	Há uma prova para você realizar.
	Use este link[1] para poder acessar a mesma. Ele irá expirar em [2]{0}!

	[1]{0}

	Este é um email automático, não o responda!
	"""
	msg.set_content(content.format(link, expiration))
	print(token)
	asparagus_cid = make_msgid()

	content = """\
	<html>
	  <head></head>
	  <body>
		<p>Olá,</p>
		<p>Há uma prova para você realizar.</br>
		Use este <a href="{0}">link</a> para poder acessar a mesma. Ele irá expirar em {1}!</p>
		<p>Este é um email automático, não o responda!</p>
	  </body>
	</html>
	""".format(link, expiration, asparagus_cid=asparagus_cid[1:-1])

	msg.add_alternative(content, subtype='html')

	try:
		with smtplib.SMTP('localhost') as s:
			s.send_message(msg)
			return ""
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

	return ""

def getData(response):
	locals	= eval(response.get_header("locals"))
	data	= locals["data"]
	if data:
		return {
			"client_id": locals["client_id"],
			"url": "usuarios/" + data[0] + "materias/" + data[1] + "turmas/" + data[2] + "provas/" + data[3] + "realizacoes/" + data[4]
		}
	else:
		return {
			"client_id": locals["client_id"]
		}

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
