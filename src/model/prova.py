import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

from	.questao	import schema_questao, Questao
from	.realizacao	import schema_realizacao, Realizacao

schema_prova	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		},
		"descricao": {
			"type": "string"
		},
		"duracao": {
			"type": "number"
		},
		"questoes": {
			"type": "array",
			"items": schema_questao
		},
		"realizacoes": {
			"type": "array",
			"items": schema_realizacao
		},
	},
	"required": [
		"titulo"
	]
}

class ProvaType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_prova)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Prova(EmbeddedDocument):
	_id			= ObjectIdField(required=True, default=lambda: ObjectId())
	titulo		= StringField(required=True)
	descricao	= StringField()
	duracao		= IntField()
	questoes	= ListField(EmbeddedDocumentField(Questao))
	realizacoes	= ListField(EmbeddedDocumentField(Realizacao))
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
