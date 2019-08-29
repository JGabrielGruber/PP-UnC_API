from	jsonschema	import validate, exceptions
from	mongoengine	import *

schema_questao	= {
	"type":	"object",
	"properties": {
		"descricao": {
			"type": "string"
		},
		"isAlternativa": {
			"type": "boolean"
		},
		"alternativas": {
			"type": "array",
			"items": {
				"type": "string"
			}
		},
		"isMultipla": {
			"type": "boolean"
		},
		"corretas": {
			"type": "array",
			"items": {
				"type": "number"
			}
		},
		"esperado": {
			"type": "string"
		},
		"peso": {
			"type": "number"
		},
	},
	"required": [
		"descricao",
		"isAlternativa",
		"peso"
	]
}

class Questao(EmbeddedDocument):
	descricao		= StringField(required=True)
	isAlternativa	= BooleanField(required=True)
	alternativas	= ListField(StringField())
	isMultipla		= BooleanField()
	corretas		= ListField(IntField())
	esperado		= StringField()
	peso			= FloatField(max_length=2, required=True)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
