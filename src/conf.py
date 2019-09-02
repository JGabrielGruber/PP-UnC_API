import	json
import	mongoengine
import	os

def getConf():
	if not os.path.exists('./.cache'):
		os.makedirs('./.cache')
	if os.path.exists('./.cache/conf.json'):
		with open('./.cache/conf.json', mode='rb') as privatefile:
			return	json.loads(privatefile.read())['confs']
	else:
		with open('./.cache/conf.json', mode='w') as file:
			file.write(json.dumps( { "confs" : {
				"db_auth_host": "",
				"db_data_host": ""
			} } ))
			getConf()

db_auth	= mongoengine.connect(host=getConf()['db_auth_host'], alias="auth").PPUnC_Auth
db_data	= mongoengine.connect(host=getConf()['db_data_host'], alias="default").PPUnC_Data
