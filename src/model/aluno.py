from	jsonschema	import validate, exceptions
from	mongoengine	import *

schema_aluno	= {
	"type":	"object",
	"properties": {
		"nome": {
			"type": "string"
		},
		"email": {
			"type": "string"
		}
	},
	"required": [
		"nome",
		"email"
	]
}

class Aluno(EmbeddedDocument):
	nome	= StringField(required=True)
	email	= StringField(required=True)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
