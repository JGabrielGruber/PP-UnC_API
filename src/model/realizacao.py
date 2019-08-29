from	jsonschema	import validate, exceptions
from	mongoengine	import *

from	.aluno		import schema_aluno, Aluno

schema_realizacao	= {
	"type":	"object",
	"properties": {
		"aluno": schema_aluno,
		"resposta": {
			"type": "array",
			"items": schema_resposta
		},
		"finalizada": {
			"type": "boolean"
		},
		"total": {
			"type": "number"
		}
	},
	"required": [
		"aluno"
	]
}

class Realizacao(EmbeddedDocument):
	aluno			= EmbeddedDocumentField(Aluno)
	resposta		= ListField(EmbeddedDocumentField(Resposta))
	correta			= BooleanField()
	meioCorreta		= BooleanField()
