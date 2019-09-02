import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

from	.aluno	import schema_aluno, Aluno
from	.prova	import schema_prova, Prova
from	.curso	import schema_curso, Curso

schema_turma	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		},
		"descricao": {
			"type": "string"
		},
		"curso": schema_curso,
		"ano": {
			"type": "number"
		},
		"semestre": {
			"type": "number"
		},
		"alunos": {
			"type": "array",
			"items": schema_aluno
		},
		"provas": {
			"type": "array",
			"items": schema_prova
		},
	},
	"required": [
		"titulo"
	]
}

class TurmaType(hug.types.Type):
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

class Turma(EmbeddedDocument):
	titulo		= StringField(required=True)
	descricao	= StringField()
	curso		= ReferenceField('Curso', reverse_delete_rule=DO_NOTHING)
	ano			= IntField()
	semestre	= IntField()
	alunos		= ListField(EmbeddedDocumentField(Aluno))
	provas		= ListField(EmbeddedDocumentField(Prova))
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
