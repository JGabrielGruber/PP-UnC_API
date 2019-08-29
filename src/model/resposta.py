from	jsonschema	import validate, exceptions
from	mongoengine	import *

schema_resposta	= {
	"type":	"object",
	"properties": {
		"escolhas": {
			"type": "array",
			"items": {
				"type": "number"
			}
		},
		"resposta": {
			"type": "string"
		},
		"correta": {
			"type": "boolean"
		},
		"meioCorreta": {
			"type": "boolean"
		}
	}
}

class Resposta(EmbeddedDocument):
	escolhas		= ListField(IntField())
	resposta		= StringField()
	correta			= BooleanField()
	meioCorreta		= BooleanField()
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
