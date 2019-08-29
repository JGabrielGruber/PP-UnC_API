from	jsonschema	import validate, exceptions
from	mongoengine	import *

schema_aluno	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		}
	},
	"required": [
		"titulo"
	]
}

class Aluno(EmbeddedDocument):
	titulo	= StringField(required=True)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
