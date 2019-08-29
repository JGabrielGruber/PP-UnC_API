from	jsonschema	import validate, exceptions
from	mongoengine	import *

from	.questao	import schema_questao, Questao

schema_prova_base	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		},
		"descricao": {
			"type": "string"
		},
		"questao": {
			"type": "array",
			"items": schema_questao
		}
	},
	"required": [
		"titulo"
	]
}

class ProvaBase(EmbeddedDocument):
	titulo		= StringField(required=True)
	descricao	= StringField(required=True)
	questao		= ListField(EmbeddedDocumentField(Questao))
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
