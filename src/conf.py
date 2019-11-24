import	json
import	mongoengine
import	os
import	time

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
				"db_data_host": "",
				"web_url": "",
				"smtp_url": "",
				"smtp_port": "",
				"smtp_user": "",
				"smtp_password": "",
			} } ))
			getConf()

def connectDB():
	try:
		db_auth	= mongoengine.connect('PPUnCAuth', host=getConf()['db_auth_host'], alias="auth")
		db_data	= mongoengine.connect('PPUnC', host=getConf()['db_data_host'], alias="default")
	except Exception as e:
		print(e)
		time.sleep(10)
		print("Retrying to connect...")
		connectDB()

connectDB()
